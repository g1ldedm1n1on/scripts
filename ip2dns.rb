#! /usr/bin/env ruby
require 'resolv'
require 'colored'


ips = $stdin.read
#ips = ips.to_s
ips = ips.chop!
ips = ips.strip

ips.each_line do |ip|
	ip = ip.to_s
	ip = ip.chop!

	begin

	dns = Resolv.getname(ip)
rescue Exception => e
	dns = '<Failed to Resolve Name>'
end
if dns == '<Failed to Resolve Name>'
	puts '<Did not Resolve Name>'.red + ':' + ip
else
puts dns + ':' + ip
end
end
