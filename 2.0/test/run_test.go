package test

import (
	"path"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/openshift/imagetest"
)

const BuilderImage = "openshift/ruby-20-centos7-candidate"

var RepoRoot string

func init() {
	_, filename, _, _ := runtime.Caller(1)
	RepoRoot = path.Dir(path.Dir(path.Dir(filename)))
}

func TestRubyHelloWorld(t *testing.T) {
	t.Parallel()
	imagetest.TestImageFromSource(t, BuilderImage, "git://github.com/openshift/ruby-hello-world.git", "", "sti-ruby-test/ruby-hello-world")
}

func TestPuma(t *testing.T) {
	t.Parallel()
	imagetest.TestImageFromSource(t, BuilderImage, RepoRoot, filepath.Join("2.0", "test", "puma-test-app"), "sti-ruby-test/puma-test-app")
}

func TestRack(t *testing.T) {
	t.Parallel()
	imagetest.TestImageFromSource(t, BuilderImage, RepoRoot, filepath.Join("2.0", "test", "rack-test-app"), "sti-ruby-test/rack-test-app")
}
