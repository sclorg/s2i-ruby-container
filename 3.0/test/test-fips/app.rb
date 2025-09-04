require 'sinatra'
require 'openssl'

set :server, 'webrick'

MESSAGE = "My secret text\n".freeze

get '/' do
  exit 0
end

get '/symmetric/aes-256-cbc' do
  # This should pass with and without FIPS.
  cipher = OpenSSL::Cipher.new('aes-256-cfb')
  cipher.encrypt
  cipher.random_key
  cipher.random_iv
  enc = cipher.update(MESSAGE) + cipher.final
  return 200, enc
rescue => e
  return 409, "Unexpected failure with aes-256-cbc, fips #{fips_state}, #{e.inspect}\nBacktrace:\n#{e.backtrace}\n"
end

get '/symmetric/des-ede-cbc' do
  status = 200

  cipher = OpenSSL::Cipher.new('des-ede-cbc')
  cipher.encrypt
  # This fails in FIPS only once we try to get a key for the 3DES.
  cipher.random_key
  cipher.random_iv
  cipher.update(MESSAGE) + cipher.final
rescue OpenSSL::Cipher::CipherError => e
  return status, "Failed with fips #{fips_state} #{e.inspect}\n" if OpenSSL.fips_mode

  return 500, "Failed with fips #{fips_state} #{e.inspect}\nBacktrace:\n#{e.backtrace}\n"
rescue => e
  return 409, "Unexpected failure with des-ede-cbc, fips #{fips_state}, #{e.inspect}\nBacktrace:\n#{e.backtrace}\n"
end

get '/hash/sha256' do
  status = 200
  message = "SHA256 succeeded, fips is #{fips_state}"

  fips_state = OpenSSL.fips_mode ? 'enabled' : 'disabled'

  OpenSSL::Digest.digest('SHA256', MESSAGE)

  return status, message
rescue => e
  return 409, "Unexpected failure with SHA256, fips #{fips_state}, #{e.inspect}\nBacktrace:\n#{e.backtrace}\n"
end

get '/hash/md5' do
  status = 200
  message = "MD5 succeeded, fips is #{fips_state}"

  fips_state = OpenSSL.fips_mode ? 'enabled' : 'disabled'

  OpenSSL::Digest.digest('MD5', MESSAGE)

  # FIPS is on, but this passed, that shouldn't be the case.
  status = 500 unless OpenSSL.fips_mode

  return status, message
rescue OpenSSL::Digest::DigestError => e
  return status, "Failed with fips #{fips_state} #{e.inspect}\n" if OpenSSL.fips_mode

  return 500, "Failed with fips #{fips_state} #{e.inspect}\nBacktrace:\n#{e.backtrace}\n"
rescue => e
  return 409, "Unexpected failure with MD5, fips #{fips_state}, #{e.inspect}\nBacktrace:\n#{e.backtrace}\n"
end
