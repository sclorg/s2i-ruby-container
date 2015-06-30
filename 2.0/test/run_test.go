package test

import (
	"os/exec"
	"path"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/openshift/sti-ruby/2.0/test/imagetest"
)

var TestDir string

func init() {
	_, filename, _, _ := runtime.Caller(1)
	TestDir = path.Dir(filename)
}

func TestRubyHelloWorld(t *testing.T) {
	t.Parallel()
	if !imagetest.ReuseImages {
		cmd := exec.Command("git", "clone", "git://github.com/openshift/ruby-hello-world.git")
		cmd.Dir = TestDir
		b, err := cmd.CombinedOutput()
		if err != nil {
			t.Fatalf("\n%s\n%s", b, err)
		}
	}
	imagetest.TestImageFromSource(t, filepath.Join(TestDir, "ruby-hello-world"))
}

func TestPuma(t *testing.T) {
	t.Parallel()
	imagetest.TestImageFromSource(t, filepath.Join(TestDir, "puma-test-app"))
}

func TestRack(t *testing.T) {
	t.Parallel()
	imagetest.TestImageFromSource(t, filepath.Join(TestDir, "rack-test-app"))
}
