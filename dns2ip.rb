#! /usr/bin/env ruby
require 'resolv'
require 'colored'


dns = $stdin.read
dns = dns.chop!
dns = dns.strip

dns.each_line do |i|
        i = i.to_s
        i = i.chop!

        begin

        ip = Resolv.getaddress(i)
rescue Exception => e
        ip = '<Failed to Lookup IP>'
end
if ip == '<Failed to Lookup IP>'
        puts '<Failed to Lookup IP>'.red + ':' + i
else
puts ip + ':' + i
end
end