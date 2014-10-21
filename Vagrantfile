# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'fileutils'

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'robmadole/jig-development'

  # Use a private network so NFS can do its thing
  config.vm.network "private_network", type: "dhcp"

  # Disable the default share
  config.vm.synced_folder '.', '/vagrant', disabled: true
  # Use the name of the project
  config.vm.synced_folder '.', '/lure', type: 'nfs'
  # Configured for Salt
  config.vm.synced_folder 'salt/roots/', '/srv', type: 'nfs'

  # Make sure that the user-specific .lure directory exists
  users_specs = File.expand_path('~/.lure/specs')
  FileUtils.mkpath users_specs

  # Local user-specific directory to hold Lure specs and projects
  config.vm.synced_folder users_specs, '/specs', type: 'nfs'

  config.vm.provision :salt do |salt|
    salt.minion_config = 'salt/minion'
    salt.run_highstate = true
    salt.install_type  = 'git'
    salt.install_args  = 'v2014.1.13'
  end
end
