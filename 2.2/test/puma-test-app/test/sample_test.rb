require 'bundler'
require 'minitest/autorun'

class TestSample < Minitest::Unit::TestCase
  def test_sample
    assert_equal "Foo", "Foo"
  end
end
