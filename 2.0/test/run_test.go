package test

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"testing"
	"time"
)

var ImageName string
var TestDir string

var ReuseImages bool

func init() {
	ImageName = os.Getenv("IMAGE_NAME")
	if ImageName == "" {
		ImageName = "openshift/ruby-20-centos7-candidate"
	}
	_, filename, _, _ := runtime.Caller(1)
	TestDir = path.Dir(filename)

	flag.BoolVar(&ReuseImages, "reuseimages", false,
		"reuse existing Docker images of test applications")
}

type TestCase struct {
	*testing.T
	testApp     string
	ImageName   string
	ContainerID string
	ContainerIP string
}

func NewTestCase(testApp string, t *testing.T) *TestCase {
	return &TestCase{
		T:         t,
		testApp:   testApp,
		ImageName: fmt.Sprintf("sti-ruby-test/%s", testApp),
	}
}

func (tc *TestCase) BuildTestApp() ([]byte, error) {
	tc.Log("building...")
	path := filepath.Join(TestDir, tc.testApp)
	cmd := exec.Command("sti", "build", "--force-pull=false",
		path, ImageName, tc.ImageName)
	b, err := cmd.CombinedOutput()
	return b, err
}

func (tc *TestCase) RunTestApp() ([]byte, error) {
	cmd := exec.Command("docker", "run",
		"--user=100001", "-p", "8080", "-d",
		tc.ImageName)
	b, err := cmd.CombinedOutput()
	if err != nil {
		return b, err
	}
	tc.ContainerID = strings.TrimSpace(string(b))
	return tc.InspectContainerIP()
}

func (tc *TestCase) InspectContainerIP() ([]byte, error) {
	cmd := exec.Command("docker", "inspect",
		"--format='{{ .NetworkSettings.IPAddress }}'", tc.ContainerID)
	b, err := cmd.CombinedOutput()
	if err != nil {
		return b, err
	}
	tc.ContainerIP = strings.TrimSpace(string(b))
	return b, err
}

func (tc *TestCase) StopTestApp() ([]byte, error) {
	cmd := exec.Command("docker", "stop", tc.ContainerID)
	b, err := cmd.CombinedOutput()
	return b, err
}

func (tc *TestCase) CheckHTTPConnectivity() {
	client := &http.Client{
		Timeout: 10 * time.Second,
	}
	url := fmt.Sprintf("http://%s:8080", tc.ContainerIP)
	var err error
	for attempt := 0; attempt < 10; attempt++ {
		resp, err := client.Head(url)
		if err != nil {
			// tc.Logf("HTTP connection attempt #%d failed: %s", attempt, err)
			time.Sleep(1 * time.Second)
			continue
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusOK {
			tc.Errorf("got %v; wanted %v",
				resp.StatusCode, http.StatusOK)
		}
		return
	}
	tc.Error(err)
}

func (tc *TestCase) CheckSCLEnabled() {
	// time.Sleep(1 * time.Second)
	// tc.Errorf("SCLEnabled error")
	// TODO implement this
}

func runTestCase(testApp string, t *testing.T) {
	tc := NewTestCase(testApp, t)
	if !ReuseImages {
		b, err := tc.BuildTestApp()
		if err != nil {
			if b != nil {
				tc.Fatalf("\n%s\n%s", b, err)
			}
			tc.Fatal(err)
		}
	}
	b, err := tc.RunTestApp()
	if err != nil {
		if b != nil {
			tc.Fatalf("\n%s\n%s", b, err)
		}
		tc.Fatal(err)
	}
	defer tc.StopTestApp()
	Parallel([]func(){
		tc.CheckHTTPConnectivity,
		tc.CheckSCLEnabled,
	})
}

func Parallel(fs []func()) {
	var wg sync.WaitGroup
	for _, f := range fs {
		f := f
		wg.Add(1)
		go func() {
			f()
			wg.Done()
		}()
	}
	wg.Wait()
}

func TestRubyHelloWorld(t *testing.T) {
	t.Parallel()
	cmd := exec.Command("bash", "-c",
		"[ -d ruby-hello-world ] && cd ruby-hello-world && git pull || "+
			"git clone git://github.com/openshift/ruby-hello-world.git")
	cmd.Dir = TestDir
	b, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("\n%s\n%s", b, err)
	}
	runTestCase("ruby-hello-world", t)
}

func TestPuma(t *testing.T) {
	t.Parallel()
	runTestCase("puma-test-app", t)
}

func TestRack(t *testing.T) {
	t.Parallel()
	runTestCase("rack-test-app", t)
}
