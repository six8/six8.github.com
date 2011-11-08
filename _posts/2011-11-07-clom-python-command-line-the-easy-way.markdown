--- 
layout: post
comments: true
title: "Clom: Python command line the easy way"
date: Mon Nov 07 23:58:43 -0600 2011
---

Now Just WTF is Clom?
---------------------

Clom is a Python Command Line Object Mapper. I wrote [Clom][clom] in order to reduce the amount of repetitive coding needed to write apps that routinely deal with the command line. [Fabric][fabric] scripts in particular involve string manipulation to write commands which can lead to error prone, unescaped, and unsafe commands. Instead of working directly with strings and having to worry about escaping arguments yourself (or completely forgetting to), Clom allows you to work with an object interface to write commands more safely. Just as SQL ORMs allow you to write re-usable and safer SQL, Clom allows you to write re-usable and safer command line code.

Using Clom to Manage VirtualBox
-------------------------------

To introduce you to Clom and how it's useful, let's take a look at how we could use Clom to manage some [VirtualBoxes][virtualbox].

	>>> from clom import clom
	>>> clom.VBoxManage.list.runningvms()
	'VBoxManage list runningvms'

Working with Clom starts with the clom object. Commands are accessed by attribute or item lookup. Each command can have sub-commands also accessed by attribute or item lookup. Calling a command doesn't execute it. A command can be stringified in order to be passed to a [subprocess][subprocess] function, Popen, or even [Fabric][fabric]. Clom also offers a shortcut for easily executing commands in a shell.

	>>> clom.VBoxManage.list.runningvms.shell()
	INFO:clom.shell:Executing command: VBoxManage list runningvms
	<CommandResult return_code=0, stdout=0 bytes, stderr=0 bytes>

### Shelling Out Commands

The Clom [shell interface](http://clom.readthedocs.org/en/latest/api.html#shell) offers many convenient ways to access the return result of a shell command.

	>>> clom.VBoxManage.list.vms.shell.all()
	INFO:clom.shell:Executing command: VBoxManage list vms
	['"Windows Base" {949ec0af-92d0-4140-8a6c-36301ca6f695}', '"Dev_1320289635" {0a4df13c-e9f8-42c1-b09b-1f4619cca34d}']


	>>> clom.VBoxManage.list.vms.shell.first()
	INFO:clom.shell:Executing command: VBoxManage list vms
	'"Windows Base" {949ec0af-92d0-4140-8a6c-36301ca6f695}'


	>>> clom.VBoxManage.list.vms.shell.last()
	INFO:clom.shell:Executing command: VBoxManage list vms
	'"Dev_1320289635" {0a4df13c-e9f8-42c1-b09b-1f4619cca34d}'

You can also iterate over the lines of the command's results.

	>>> for line in clom.VBoxManage.list.vms.shell():
	...     print line
	... 
	INFO:clom.shell:Executing command: VBoxManage list vms
	"Windows Base" {949ec0af-92d0-4140-8a6c-36301ca6f695}
	"Dev_1320289635" {0a4df13c-e9f8-42c1-b09b-1f4619cca34d}

Shell execution returns [CommandResult](http://clom.readthedocs.org/en/latest/api.html#clom.shell.CommandResult) which allows access to stdout, stderr, and the return code of the command.

### Augment with Arguments

Commands aren't very interesting without arguments, so let's add some.

	>>> clom.VBoxManage.showvminfo('Windows Base', machinereadable=True, details=True).shell.all()[:5]
	INFO:clom.shell:Executing command: VBoxManage showvminfo --machinereadable --details 'Windows Base'
	['name="Windows Base"', 'ostype="WindowsXP"', 'UUID="949ec0af-92d0-4140-8a6c-36301ca6f695"', 'CfgFile="VirtualBox/Machines/Windows Base/Windows Base.xml"', 'SnapFldr="VirtualBox/Machines/Windows Base/Snapshots"']

There's several ways to add arguments and options. When arguments or option values are used, they're properly escaped if needed.

	>>> name = 'Test VM'
 	>>> clom.VBoxManage.createvm(name=name, register=True, ostype='Linux').shell.all()
	INFO:clom.shell:Executing command: VBoxManage createvm --ostype Linux --register --name 'Test VM'
	["Virtual machine 'Test VM' is created and registered.", 'UUID: e7b73b54-7a94-4aaa-9f5f-335140a1703a', "Settings file: 'VirtualBox VMs/Test VM/Test VM.vbox'"]

Options can be specified by calling a command with keyword arguments as above or by using `with_opts()`. Options and arguments have a catch however. Options are always listed before arguments. VBoxManage expects the VM's name as the first argument, followed by options. 

	>>> clom.VBoxManage.modifyvm('Test VM').with_opts('--vrde', 'on', memory=256, usb='on')
    'VBoxManage modifyvm --vrde on --usb on --memory 256 'Test VM''

Unfortunately, as expected, the code above puts the VM name after the options. We can get around this by passing the VM name as the first option. `with_opts()` honors positional options followed by unspecified order keyword options.

	>>> clom.VBoxManage.modifyvm.with_opts('Test VM', '--vrde', 'on', memory=256, usb='on')
	'VBoxManage modifyvm 'Test VM' --vrde on --usb on --memory 256'

Arguments are straight forward. They're just added to the end of the command in the order you provide.

	>>> clom.VBoxManage.registervm.with_args('/path/to/vm')
	'VBoxManage registervm /path/to/vm'


	>>> clom.VBoxManage.setproperty.with_args('machinefolder', 'default')
	'VBoxManage setproperty machinefolder default'

Calling a command is simply an alias to `with_opts(**kwargs).with_args(*args)`. The above could also be written as a function call.

	>>> clom.VBoxManage.registervm('/path/to/vm')
	'VBoxManage registervm /path/to/vm'


	>>> clom.VBoxManage.setproperty('machinefolder', 'default')
	'VBoxManage setproperty machinefolder default'

### Reusing Clom Objects

Part of the power of Clom is that each command object is re-usable. This allows you to chain and combine commands or use them many times for batch commands.

	>>> vbox = clom.VBoxManage
	>>> vbox.list.runningvms
	'VBoxManage list runningvms'

Sub-commands can be re-used as well.

	>>> list = vbox.list
	>>> list.runningvms
	'VBoxManage list runningvms'	
	>>> list.vms
	'VBoxManage list vms'	
	>>> list.dvds
	'VBoxManage list dvds'	

You can set default options and arguments.

	>>> create_linux = vbox.createvm.with_opts(ostype='Linux')
	>>> create_linux(name='My Box')
	'VBoxManage createvm --ostype Linux --name 'My Box''
	>>> create_linux(name='Their Box')
	'VBoxManage createvm --ostype Linux --name 'Their Box''

### Background Noise

Some commands need to be forked and ran in the background.

	>>> clom.VBoxHeadless.with_opts(startvm='Test VM').background().shell()
	INFO:clom.shell:Executing command (capture off): nohup VBoxHeadless --startvm 'Test VM' &> /dev/null &
	<CommandResult return_code=0, stdout=0 bytes, stderr=0 bytes>

	>>> vbox.controlvm.with_opts('Test VM').with_args('poweroff').shell()
	INFO:clom.shell:Executing command: VBoxManage controlvm 'Test VM' poweroff
	
### Shortcuts

Clom has shortcuts for most POSIX operations including:

* `with_env` - Run the operation with environmental variables
* `hide_output` - Redirect a command's file descriptors to /dev/null
* `output_to_file` - Replace a file's contents with this command's output
* `append_to_file` - Append this command's output to a file
* `pipe_to` - Pipe this command to another

See the [API docs](http://clom.readthedocs.org/en/latest/api.html) for details.

### Fabric

Clom's original inspiration came from doing lots of automation with [Fabric][fabric].

	>>> from fabric.api import local
	>>> vbox = clom.VBoxManage
	>>> local(vbox.list.vms)
	[localhost] local: VBoxManage list vms

This of course means you can use Clom with Fabric tasks, including remote ones.

	>>> def vmstart(name):
	>>> ... run(vbox.startvm(name))
	
Clom even understands how to create Fabric commands.

	>>> clom.fab.vmstart('dev')
	'fab vmstart:dev'

	>>> clom.fab.vmstart('dev').vmstartservice('dev', 'nginx', 'flask')
	'fab vmstart:dev vmstartservice:dev,nginx,flask'

That's It
---------

I hope you've found this introduction to Clom useful. Check out [Clom's Documentation](http://clom.readthedocs.org/en/latest/index.html) for other ways to use Clom and fork [Clom on Github][clom].

[clom]: http://github.com/six8/python-clom
[fabric]: http://fabfile.org/
[subprocess]: http://docs.python.org/library/subprocess.html
[virtualbox]: http://www.virtualbox.org/