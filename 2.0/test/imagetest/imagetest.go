package imagetest

import (
	"flag"
	"fmt"
	"net/http"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"
)

var (
	BuilderImage string
	ReuseImages  bool
)

func init() {
	flag.StringVar(&BuilderImage, "builderimage",
		"openshift/ruby-20-centos7-candidate",
		"builder image used to build test applications")
	flag.BoolVar(&ReuseImages, "reuseimages", false,
		"reuse existing Docker images of test applications")
}

func BuildApp(path, builderImage, outputImage string) ([]byte, error) {
	cmd := exec.Command("sti", "build", "--force-pull=false",
		path, builderImage, outputImage)
	b, err := cmd.CombinedOutput()
	return b, err
}

func RunApp(imageName string) (string, error) {
	cmd := exec.Command("docker", "run",
		"--user=12345", "-p", "8080", "-d", imageName)
	b, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("%s: %s", err, b)
	}
	containerID := strings.TrimSpace(string(b))
	return containerID, nil
}

func InspectContainerIP(containerID string) (string, error) {
	cmd := exec.Command("docker", "inspect",
		"--format='{{ .NetworkSettings.IPAddress }}'", containerID)
	b, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("%s: %s", err, b)
	}
	return strings.TrimSpace(string(b)), nil
}

func StopTestApp(containerID string) error {
	cmd := exec.Command("docker", "rm", "-f", containerID)
	b, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("%s: %s", err, b)
	}
	return nil
}

func CheckHTTPConnectivity(url string) error {
	var (
		resp *http.Response
		err  error
	)
	const maxAttempts = 10
	client := &http.Client{
		Timeout: 10 * time.Second,
	}
	for attempt := 0; attempt < maxAttempts; attempt++ {
		resp, err = client.Head(url)
		if err != nil {
			time.Sleep(1 * time.Second)
			continue
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusOK {
			return fmt.Errorf("HTTP status: got %v; wanted %v",
				resp.StatusCode, http.StatusOK)
		}
		return nil
	}
	return fmt.Errorf("failed after %d attempts: %v", maxAttempts, err)
}

func CheckSCLEnabled() error {
	// time.Sleep(1 * time.Second)
	// tc.Errorf("SCLEnabled error")
	// TODO implement this
	return nil
}

func TestImageFromSource(t *testing.T, path string) {
	outputImage := fmt.Sprintf("sti-ruby-test/%s", filepath.Base(path))
	if !ReuseImages {
		b, err := BuildApp(path, BuilderImage, outputImage)
		if err != nil {
			if b != nil {
				t.Fatalf("\n%s\n%s", b, err)
			}
			t.Fatal(err)
		}
	}
	containerID, err := RunApp(outputImage)
	if err != nil {
		t.Fatal(err)
	}
	defer StopTestApp(containerID)
	containerIP, err := InspectContainerIP(containerID)
	if err != nil {
		t.Fatal(err)
	}
	Parallel([]func() error{
		func() error {
			url := fmt.Sprintf("http://%s:8080", containerIP)
			return CheckHTTPConnectivity(url)
		},
		CheckSCLEnabled,
	}, t)
}

func Parallel(fs []func() error, t *testing.T) {
	var wg sync.WaitGroup
	for _, f := range fs {
		f := f
		wg.Add(1)
		go func() {
			err := f()
			if err != nil {
				t.Error(err)
			}
			wg.Done()
		}()
	}
	wg.Wait()
}
