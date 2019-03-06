#-*-coding=utf-8-*-
# Auto Configure Centos Network Service.
# Project Start Date : 2019-2-21.
# Author : 云汐zql.
# Call me as QQ : 1838115594 Or Wechat : Pirate_Team.
import os, sys, socket
#=============================================================#
#OS_V = 'C7'
OS_V = 'C6'
edit = "gedit "
Show_Log = 0
Sys_Init_Status = 1

# Sys_Init(make_yum_source, selinux_status, iptables_status, iptables_enable, iptables_configure, ipforward_status)
Sys_Init_Options = [1,0,1,1,1,1]

# Services_List = [Samba, Postfix, NFS, NIS, FTP] # Postfix 不能与 Sendmail同时运行。
Services_List = [1,1,1,1,0]

# Services_List0 = [Apache, Bind, Unbound, PXE, Sendmail] # Postfix 不能与 Sendmail同时运行。
Services_List0 = [1,1,0,1,0]
#-------------------------------------
# Postfix_Options(myhostname, mydomain, network, mailbox_size=50, message_size=10)
Postfix_Options = ['localhost', 'localdoamin', '10.10.10.0/24,0.0.0.0/0', 50 ,10]
# PXE_Server(dhcp_domain, dhcp_network, dhcp_netmask, dhcp_netrange, dns_domain, dns_addr, default_router, min_release, max_release, pxe_nexttop, tftp_boot_root, ftp_root)
Pxe_Options = ['mydhcpdomain', '10.10.10.0', '255.255.255.0', '10.10.10.100 10.10.10.200', 'dns.netskills.net', '114.114.114.114', '10.10.10.254', '172800', '259200', '10.10.10.1', '/tftpboot', '/var/ftp/pub']
# Bind (hostname, domain_name, arpa_area='0.0.0.127')
Bind_Options = ['dns', 'zeronet.club', '0.10.10.10']
# Ftp_Options(Virtual_UserName, Virtual_Path, Virtual_User_Conf, Ftp_Path, SSL_Enable)
Ftp_Options = ['admin', '/home/vsftpd', '/etc/vsftpd/vsftpd_user_config_dir', '/var/ftpsite', 'no']
# Nis_Options(nisdomain)
Nis_Options = ['test.com']
# Sendmail_Options(MaxMessageSize, hostname)
Sendmail_Options = [5, "test.com"]
# Ppache_configure(virtualhostname, webroot, ssl)
Apache_Options = ['www.zeronet.club', '/var/www/html/', 'no']
#=============================================================#
def Service(Srvname, action):
    if OS_V == "C7":
        os.system("systemctl " + action + " " + Srvname)
    else:
        os.system("service " + Srvname + " " + action)

def Auto_Enable(Srvname, action):
    if action == "on":
        systemctl_enable = 'enable'
        chkconfig_enable = 'on'
    if action == "off":
        systemctl_enable = 'disable'
        chkconfig_enable = 'off'
    if OS_V == "C7":
        os.system("systemctl " + action + " " + Srvname)
    else:
        os.system("chkconfig " + Srvname + " " + action)

def Sys_Init(make_yum_source=1,selinux_status=0,iptables_status=1,iptables_enable=1,iptables_configure=0,ipforward_status=0):
    global edit
    yum_repo = """
[1]
name=1
enable=1
gpgcheck=0
baseurl=file:///mnt/src""" 
    if make_yum_source == 1:
        os.system("mkdir /mnt/src")
        os.system("mount /dev/cdrom /mnt/src")
        os.system("mount /dev/cdrom1 /mnt/src")
        os.system("rm -rf /etc/yum.repos.d/*")
        os.system("touch /etc/yum.repos.d/1.repo")
        f = open("/etc/yum.repos.d/1.repo","w+")
        f.write(yum_repo)
        f.close()
        os.system("yum makecache")
        os.system("yum install openssl -y ; yum install mod_ssl -y ; yum install vim -y ; yum install gedit -y")
    if selinux_status == 0:
        offon = "disabled"
    else:
        offon = "enforcing"
    selinux_config = """
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=""" + offon + """
# SELINUXTYPE= can take one of these two values:
#     targeted - Targeted processes are protected,
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted 
    """
    f = open("/etc/selinux/config","w+")
    f.write(selinux_config)
    f.close()
    os.system("setenforce 0")
    if iptables_status == 0:
        Service('iptables','stop')
    if iptables_enable == 0:
        Auto_Enable('iptables','off')
    if ipforward_status == 1:
        os.system("echo 1 >/proc/sys/net/ipv4/ip_forward")
        sysctl_config = """
# Kernel sysctl configuration file for Red Hat Linux
# For binary values, 0 is disabled, 1 is enabled.  See sysctl(8) and
# sysctl.conf(5) for more details.
# Controls IP packet forwarding
net.ipv4.ip_forward = 1
# Controls source route verification
net.ipv4.conf.default.rp_filter = 1
# Do not accept source routing
net.ipv4.conf.default.accept_source_route = 0
# Controls the System Request debugging functionality of the kernel
kernel.sysrq = 0
# Controls whether core dumps will append the PID to the core filename.
# Useful for debugging multi-threaded applications.
kernel.core_uses_pid = 1
# Controls the use of TCP syncookies
net.ipv4.tcp_syncookies = 1
# Disable netfilter on bridges.
net.bridge.bridge-nf-call-ip6tables = 0
net.bridge.bridge-nf-call-iptables = 0
net.bridge.bridge-nf-call-arptables = 0
# Controls the default maxmimum size of a mesage queue
kernel.msgmnb = 65536
# Controls the maximum size of a message, in bytes
kernel.msgmax = 65536
# Controls the maximum shared segment size, in bytes
kernel.shmmax = 68719476736
# Controls the maximum number of shared memory segments, in pages
kernel.shmall = 4294967296
"""
        f = open("/etc/sysctl.conf","w+")
        f.write(sysctl_config)
        f.close()
    if iptables_configure == 1:
        Sour_Iptables_List = """
# Example :
#   -A INPUT -p tcp --dport 22 -j ACCEPT
#   -A OUTPUT -p tcp --sport 22 -j ACCEPT

#   -A INPUT -i lo -p all -j ACCEPT # Allow Loopback.
#   -A OUTPUT -o lo -p all -j ACCEPT

-P INPUT ACCEPT
-P OUTPUT ACCEPT
-P FORWARD DROP
"""
        with open("/etc/iptables.rulelist","w+") as f:
            f.write(Sour_Iptables_List)
        os.system(edit + " /etc/iptables.rulelist")
        with open("/etc/iptables.rulelist","r") as f:
            Iptables_List = f.read()

        iptables_conf = """
# Generated by iptables-save v1.4.7 on Fri Feb 15 18:23:35 2019
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
""" + Iptables_List + """
COMMIT
# Completed on Fri Feb 15 18:23:35 2019
"""     
        Service('iptables','stop')
        f = open("/etc/sysconfig/iptables","w+")
        f.write(iptables_conf)
        f.close()
        Service('iptables','restart')

def nfs_configure():
    os.system("yum install nfs-utils -y")
    os.system("yum install rpcbind -y")
    NFS_Shared_List = """
# ro：目录只读
# rw：目录读写
# sync：将数据同步写入内存缓冲区与磁盘中，效率低，但可以保证数据的一致性
# async：将数据先保存在内存缓冲区中，必要时才写入磁盘
# all_squash：将远程访问的所有普通用户及所属组都映射为匿名用户或用户组(nfsnobody)
# no_all_squash：与all_squash取反(默认设置)
# root_squash：将root用户及所属组都映射为匿名用户或用户组(默认设置)
# no_root_squash：与rootsquash取反
# anonuid=xxx：将远程访问的所有用户都映射为匿名用户，并指定该用户为本地用户(UID=xxx)
# anongid=xxx：将远程访问的所有用户组都映射为匿名用户组账户
/home 192.168.0.0/16(rw)
/home 0.0.0.0/0(ro)
/var/tmp 0.0.0.0/0(rw,no_root_squash)
# mount -t nfs 192.168.1.233:/data/tmp /data/tmp2
"""
    f = open("/etc/exports","w+")
    f.write(NFS_Shared_List)
    f.close()
    os.system(edit + " /etc/exports")
    Service('rpcbind','restart')
    Service('nfs','restart')



def samba_configure():
    os.system("yum install samba -y")
    Sour_Samba_Shared_List = """
[archive]
	comment = archive
    path = /opt/shared_path
	browseable = yes
	writable = yes
	valid users = @root
    invalid users = @guest
    write list = @root
	admin users = @root
"""
    with open("/etc/samba/smb.sharelist","w+") as f:
        f.write(Sour_Samba_Shared_List)
    os.system(edit + "/etc/samba/smb.sharelist")
    with open("/etc/samba/smb.sharelist","r") as f: 
        Samba_Shared_List = f.read()
    samba_config = """
# This is the main Samba configuration file. You should read the
# smb.conf(5) manual page in order to understand the options listed
# here. Samba has a huge number of configurable options (perhaps too
# many!) most of which are not shown in this example
#
# For a step to step guide on installing, configuring and using samba, 
# read the Samba-HOWTO-Collection. This may be obtained from:
#  http://www.samba.org/samba/docs/Samba-HOWTO-Collection.pdf
#
# Many working examples of smb.conf files can be found in the 
# Samba-Guide which is generated daily and can be downloaded from: 
#  http://www.samba.org/samba/docs/Samba-Guide.pdf
#
# Any line which starts with a ; (semi-colon) or a # (hash) 
# is a comment and is ignored. In this example we will use a #
# for commentry and a ; for parts of the config file that you
# may wish to enable
#
# NOTE: Whenever you modify this file you should run the command "testparm"
# to check that you have not made any basic syntactic errors. 
#
#---------------
# SELINUX NOTES:
#
# If you want to use the useradd/groupadd family of binaries please run:
# setsebool -P samba_domain_controller on
#
# If you want to share home directories via samba please run:
# setsebool -P samba_enable_home_dirs on
#
# If you create a new directory you want to share you should mark it as
# "samba_share_t" so that selinux will let you write into it.
# Make sure not to do that on system directories as they may already have
# been marked with othe SELinux labels.
#
# Use ls -ldZ /path to see which context a directory has
#
# Set labels only on directories you created!
# To set a label use the following: chcon -t samba_share_t /path
#
# If you need to share a system created directory you can use one of the
# following (read-only/read-write):
# setsebool -P samba_export_all_ro on
# or
# setsebool -P samba_export_all_rw on
#
# If you want to run scripts (preexec/root prexec/print command/...) please
# put them into the /var/lib/samba/scripts directory so that smbd will be
# allowed to run them.
# Make sure you COPY them and not MOVE them so that the right SELinux context
# is applied, to check all is ok use restorecon -R -v /var/lib/samba/scripts
#
#--------------
#
#======================= Global Settings =====================================
	
[global]
	
# ----------------------- Network Related Options -------------------------
#
# workgroup = NT-Domain-Name or Workgroup-Name, eg: MIDEARTH
#
# server string is the equivalent of the NT Description field
#
# netbios name can be used to specify a server name not tied to the hostname
#
# Interfaces lets you configure Samba to use multiple interfaces
# If you have multiple network interfaces then you can list the ones
# you want to listen on (never omit localhost)
#
# Hosts Allow/Hosts Deny lets you restrict who can connect, and you can
# specifiy it as a per share option as well
#
	workgroup = MYGROUP
	server string = Samba Server Version %v
	
;	netbios name = MYSERVER
	
;	interfaces = lo eth0 192.168.12.2/24 192.168.13.2/24 
;	hosts allow = 127. 192.168.12. 192.168.13.
	
# --------------------------- Logging Options -----------------------------
#
# Log File let you specify where to put logs and how to split them up.
#
# Max Log Size let you specify the max size log files should reach
	
	# logs split per machine
	log file = /var/log/samba/log.%m
	# max 50KB per log file, then rotate
	max log size = 50
	
# ----------------------- Standalone Server Options ------------------------
#
# Scurity can be set to user, share(deprecated) or server(deprecated)
#
# Backend to store user information in. New installations should 
# use either tdbsam or ldapsam. smbpasswd is available for backwards 
# compatibility. tdbsam requires no further configuration.

	security = user
	passdb backend = tdbsam


# ----------------------- Domain Members Options ------------------------
#
# Security must be set to domain or ads
#
# Use the realm option only with security = ads
# Specifies the Active Directory realm the host is part of
#
# Backend to store user information in. New installations should 
# use either tdbsam or ldapsam. smbpasswd is available for backwards 
# compatibility. tdbsam requires no further configuration.
#
# Use password server option only with security = server or if you can't
# use the DNS to locate Domain Controllers
# The argument list may include:
#   password server = My_PDC_Name [My_BDC_Name] [My_Next_BDC_Name]
# or to auto-locate the domain controller/s
#   password server = *
	
	
;	security = domain
;	passdb backend = tdbsam
;	realm = MY_REALM

;	password server = <NT-Server-Name>

# ----------------------- Domain Controller Options ------------------------
#
# Security must be set to user for domain controllers
#
# Backend to store user information in. New installations should 
# use either tdbsam or ldapsam. smbpasswd is available for backwards 
# compatibility. tdbsam requires no further configuration.
#
# Domain Master specifies Samba to be the Domain Master Browser. This
# allows Samba to collate browse lists between subnets. Don't use this
# if you already have a Windows NT domain controller doing this job
#
# Domain Logons let Samba be a domain logon server for Windows workstations. 
#
# Logon Scrpit let yuou specify a script to be run at login time on the client
# You need to provide it in a share called NETLOGON
#
# Logon Path let you specify where user profiles are stored (UNC path)
#
# Various scripts can be used on a domain controller or stand-alone
# machine to add or delete corresponding unix accounts
#
;	security = user
;	passdb backend = tdbsam
	
;	domain master = yes 
;	domain logons = yes
	
	# the login script name depends on the machine name
;	logon script = %m.bat
	# the login script name depends on the unix user used
;	logon script = %u.bat
;	logon path = \\%L\Profiles\%u
	# disables profiles support by specifing an empty path
;	logon path =          
	
;	add user script = /usr/sbin/useradd "%u" -n -g users
;	add group script = /usr/sbin/groupadd "%g"
;	add machine script = /usr/sbin/useradd -n -c "Workstation (%u)" -M -d /nohome -s /bin/false "%u"
;	delete user script = /usr/sbin/userdel "%u"
;	delete user from group script = /usr/sbin/userdel "%u" "%g"
;	delete group script = /usr/sbin/groupdel "%g"
	
	
# ----------------------- Browser Control Options ----------------------------
#
# set local master to no if you don't want Samba to become a master
# browser on your network. Otherwise the normal election rules apply
#
# OS Level determines the precedence of this server in master browser
# elections. The default value should be reasonable
#
# Preferred Master causes Samba to force a local browser election on startup
# and gives it a slightly higher chance of winning the election
;	local master = no
;	os level = 33
;	preferred master = yes
	
#----------------------------- Name Resolution -------------------------------
# Windows Internet Name Serving Support Section:
# Note: Samba can be either a WINS Server, or a WINS Client, but NOT both
#
# - WINS Support: Tells the NMBD component of Samba to enable it's WINS Server
#
# - WINS Server: Tells the NMBD components of Samba to be a WINS Client
#
# - WINS Proxy: Tells Samba to answer name resolution queries on
#   behalf of a non WINS capable client, for this to work there must be
#   at least one	WINS Server on the network. The default is NO.
#
# DNS Proxy - tells Samba whether or not to try to resolve NetBIOS names
# via DNS nslookups.
	
;	wins support = yes
;	wins server = w.x.y.z
;	wins proxy = yes
	
;	dns proxy = yes
	
# --------------------------- Printing Options -----------------------------
#
# Load Printers let you load automatically the list of printers rather
# than setting them up individually
#
# Cups Options let you pass the cups libs custom options, setting it to raw
# for example will let you use drivers on your Windows clients
#
# Printcap Name let you specify an alternative printcap file
#
# You can choose a non default printing system using the Printing option
	
	load printers = yes
	cups options = raw

;	printcap name = /etc/printcap
	#obtain list of printers automatically on SystemV
;	printcap name = lpstat
;	printing = cups

# --------------------------- Filesystem Options ---------------------------
#
# The following options can be uncommented if the filesystem supports
# Extended Attributes and they are enabled (usually by the mount option
# user_xattr). Thess options will let the admin store the DOS attributes
# in an EA and make samba not mess with the permission bits.
#
# Note: these options can also be set just per share, setting them in global
# makes them the default for all shares

;	map archive = no
;	map hidden = no
;	map read only = no
;	map system = no
;	store dos attributes = yes


#============================ Share Definitions ==============================

""" + Samba_Shared_List + """



[printers]
	comment = All Printers
	path = /var/spool/samba
	browseable = no
	guest ok = no
	writable = no
	printable = yes
	
# Un-comment the following and create the netlogon directory for Domain Logons
;	[netlogon]
;	comment = Network Logon Service
;	path = /var/lib/samba/netlogon
;	guest ok = yes
;	writable = no
;	share modes = no
	
	
# Un-comment the following to provide a specific roving profile share
# the default is to use the user's home directory
;	[Profiles]
;	path = /var/lib/samba/profiles
;	browseable = no
;	guest ok = yes
	
	
# A publicly accessible directory, but read only, except for people in
# the "staff" group
;	[public]
;	comment = Public Stuff
;	path = /home/samba
;	public = yes
;	writable = yes
;	printable = no
;	write list = +staff
    """
    f = open("/etc/samba/smb.conf","w+")
    f.write(samba_config)
    f.close()
    Service('smb','restart')

def postfix_configure(myhostname, mydomain, network, mailbox_size=50, message_size=10):
    Service('sendmail','stop')
    Auto_Enable('sendmail','off')
    os.system("yum install postfix -y")
    os.system("yum install dovecot -y")
    main_config = """
# Global Postfix configuration file. This file lists only a subset
# of all parameters. For the syntax, and for a complete parameter
# list, see the postconf(5) manual page (command: "man 5 postconf").
#
# For common configuration examples, see BASIC_CONFIGURATION_README
# and STANDARD_CONFIGURATION_README. To find these documents, use
# the command "postconf html_directory readme_directory", or go to
# http://www.postfix.org/.
#
# For best results, change no more than 2-3 parameters at a time,
# and test if Postfix still works after every change.

# SOFT BOUNCE
#
# The soft_bounce parameter provides a limited safety net for
# testing.  When soft_bounce is enabled, mail will remain queued that
# would otherwise bounce. This parameter disables locally-generated
# bounces, and prevents the SMTP server from rejecting mail permanently
# (by changing 5xx replies into 4xx replies). However, soft_bounce
# is no cure for address rewriting mistakes or mail routing mistakes.
#
#soft_bounce = no

# LOCAL PATHNAME INFORMATION
#
# The queue_directory specifies the location of the Postfix queue.
# This is also the root directory of Postfix daemons that run chrooted.
# See the files in examples/chroot-setup for setting up Postfix chroot
# environments on different UNIX systems.
#
queue_directory = /var/spool/postfix

# The command_directory parameter specifies the location of all
# postXXX commands.
#
command_directory = /usr/sbin

# The daemon_directory parameter specifies the location of all Postfix
# daemon programs (i.e. programs listed in the master.cf file). This
# directory must be owned by root.
#
daemon_directory = /usr/libexec/postfix

# The data_directory parameter specifies the location of Postfix-writable
# data files (caches, random numbers). This directory must be owned
# by the mail_owner account (see below).
#
data_directory = /var/lib/postfix

# QUEUE AND PROCESS OWNERSHIP
#
# The mail_owner parameter specifies the owner of the Postfix queue
# and of most Postfix daemon processes.  Specify the name of a user
# account THAT DOES NOT SHARE ITS USER OR GROUP ID WITH OTHER ACCOUNTS
# AND THAT OWNS NO OTHER FILES OR PROCESSES ON THE SYSTEM.  In
# particular, don't specify nobody or daemon. PLEASE USE A DEDICATED
# USER.
#
mail_owner = postfix

# The default_privs parameter specifies the default rights used by
# the local delivery agent for delivery to external file or command.
# These rights are used in the absence of a recipient user context.
# DO NOT SPECIFY A PRIVILEGED USER OR THE POSTFIX OWNER.
#
#default_privs = nobody

# INTERNET HOST AND DOMAIN NAMES
# 
# The myhostname parameter specifies the internet hostname of this
# mail system. The default is to use the fully-qualified domain name
# from gethostname(). $myhostname is used as a default value for many
# other configuration parameters.
#
myhostname = """ + myhostname + """
#myhostname = virtual.domain.tld

# The mydomain parameter specifies the local internet domain name.
# The default is to use $myhostname minus the first component.
# $mydomain is used as a default value for many other configuration
# parameters.
#
mydomain = """ + mydomain + """

# SENDING MAIL
# 
# The myorigin parameter specifies the domain that locally-posted
# mail appears to come from. The default is to append $myhostname,
# which is fine for small sites.  If you run a domain with multiple
# machines, you should (1) change this to $mydomain and (2) set up
# a domain-wide alias database that aliases each user to
# user@that.users.mailhost.
#
# For the sake of consistency between sender and recipient addresses,
# myorigin also specifies the default domain name that is appended
# to recipient addresses that have no @domain part.
#
myorigin = $myhostname
myorigin = $mydomain

# RECEIVING MAIL

# The inet_interfaces parameter specifies the network interface
# addresses that this mail system receives mail on.  By default,
# the software claims all active interfaces on the machine. The
# parameter also controls delivery of mail to user@[ip.address].
#
# See also the proxy_interfaces parameter, for network addresses that
# are forwarded to us via a proxy or network address translator.
#
# Note: you need to stop/start Postfix when this parameter changes.
#
inet_interfaces = all
#inet_interfaces = $myhostname
#inet_interfaces = $myhostname, localhost
#inet_interfaces = localhost

# Enable IPv4, and IPv6 if supported
inet_protocols = all

# The proxy_interfaces parameter specifies the network interface
# addresses that this mail system receives mail on by way of a
# proxy or network address translation unit. This setting extends
# the address list specified with the inet_interfaces parameter.
#
# You must specify your proxy/NAT addresses when your system is a
# backup MX host for other domains, otherwise mail delivery loops
# will happen when the primary MX host is down.
#
#proxy_interfaces =
#proxy_interfaces = 1.2.3.4

# The mydestination parameter specifies the list of domains that this
# machine considers itself the final destination for.
#
# These domains are routed to the delivery agent specified with the
# local_transport parameter setting. By default, that is the UNIX
# compatible delivery agent that lookups all recipients in /etc/passwd
# and /etc/aliases or their equivalent.
#
# The default is $myhostname + localhost.$mydomain.  On a mail domain
# gateway, you should also include $mydomain.
#
# Do not specify the names of virtual domains - those domains are
# specified elsewhere (see VIRTUAL_README).
#
# Do not specify the names of domains that this machine is backup MX
# host for. Specify those names via the relay_domains settings for
# the SMTP server, or use permit_mx_backup if you are lazy (see
# STANDARD_CONFIGURATION_README).
#
# The local machine is always the final destination for mail addressed
# to user@[the.net.work.address] of an interface that the mail system
# receives mail on (see the inet_interfaces parameter).
#
# Specify a list of host or domain names, /file/name or type:table
# patterns, separated by commas and/or whitespace. A /file/name
# pattern is replaced by its contents; a type:table is matched when
# a name matches a lookup key (the right-hand side is ignored).
# Continue long lines by starting the next line with whitespace.
#
# See also below, section "REJECTING MAIL FOR UNKNOWN LOCAL USERS".
#
mydestination = $myhostname, $mydomain
#mydestination = $myhostname, localhost.$mydomain, localhost
#mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
#mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain,
#	mail.$mydomain, www.$mydomain, ftp.$mydomain

# REJECTING MAIL FOR UNKNOWN LOCAL USERS
#
# The local_recipient_maps parameter specifies optional lookup tables
# with all names or addresses of users that are local with respect
# to $mydestination, $inet_interfaces or $proxy_interfaces.
#
# If this parameter is defined, then the SMTP server will reject
# mail for unknown local users. This parameter is defined by default.
#
# To turn off local recipient checking in the SMTP server, specify
# local_recipient_maps = (i.e. empty).
#
# The default setting assumes that you use the default Postfix local
# delivery agent for local delivery. You need to update the
# local_recipient_maps setting if:
#
# - You define $mydestination domain recipients in files other than
#   /etc/passwd, /etc/aliases, or the $virtual_alias_maps files.
#   For example, you define $mydestination domain recipients in    
#   the $virtual_mailbox_maps files.
#
# - You redefine the local delivery agent in master.cf.
#
# - You redefine the "local_transport" setting in main.cf.
#
# - You use the "luser_relay", "mailbox_transport", or "fallback_transport"
#   feature of the Postfix local delivery agent (see local(8)).
#
# Details are described in the LOCAL_RECIPIENT_README file.
#
# Beware: if the Postfix SMTP server runs chrooted, you probably have
# to access the passwd file via the proxymap service, in order to
# overcome chroot restrictions. The alternative, having a copy of
# the system passwd file in the chroot jail is just not practical.
#
# The right-hand side of the lookup tables is conveniently ignored.
# In the left-hand side, specify a bare username, an @domain.tld
# wild-card, or specify a user@domain.tld address.
# 
#local_recipient_maps = unix:passwd.byname $alias_maps
#local_recipient_maps = proxy:unix:passwd.byname $alias_maps
#local_recipient_maps =

# The unknown_local_recipient_reject_code specifies the SMTP server
# response code when a recipient domain matches $mydestination or
# ${proxy,inet}_interfaces, while $local_recipient_maps is non-empty
# and the recipient address or address local-part is not found.
#
# The default setting is 550 (reject mail) but it is safer to start
# with 450 (try again later) until you are certain that your
# local_recipient_maps settings are OK.
#
unknown_local_recipient_reject_code = 550

# TRUST AND RELAY CONTROL

# The mynetworks parameter specifies the list of "trusted" SMTP
# clients that have more privileges than "strangers".
#
# In particular, "trusted" SMTP clients are allowed to relay mail
# through Postfix.  See the smtpd_recipient_restrictions parameter
# in postconf(5).
#
# You can specify the list of "trusted" network addresses by hand
# or you can let Postfix do it for you (which is the default).
#
# By default (mynetworks_style = subnet), Postfix "trusts" SMTP
# clients in the same IP subnetworks as the local machine.
# On Linux, this does works correctly only with interfaces specified
# with the "ifconfig" command.
# 
# Specify "mynetworks_style = class" when Postfix should "trust" SMTP
# clients in the same IP class A/B/C networks as the local machine.
# Don't do this with a dialup site - it would cause Postfix to "trust"
# your entire provider's network.  Instead, specify an explicit
# mynetworks list by hand, as described below.
#  
# Specify "mynetworks_style = host" when Postfix should "trust"
# only the local machine.
# 
#mynetworks_style = class
#mynetworks_style = subnet
#mynetworks_style = host

# Alternatively, you can specify the mynetworks list by hand, in
# which case Postfix ignores the mynetworks_style setting.
#
# Specify an explicit list of network/netmask patterns, where the
# mask specifies the number of bits in the network part of a host
# address.
#
# You can also specify the absolute pathname of a pattern file instead
# of listing the patterns here. Specify type:table for table-based lookups
# (the value on the table right-hand side is not used).
#
mynetworks = """ + network + """
#mynetworks = $config_directory/mynetworks
#mynetworks = hash:/etc/postfix/network_table

# The relay_domains parameter restricts what destinations this system will
# relay mail to.  See the smtpd_recipient_restrictions description in
# postconf(5) for detailed information.
#
# By default, Postfix relays mail
# - from "trusted" clients (IP address matches $mynetworks) to any destination,
# - from "untrusted" clients to destinations that match $relay_domains or
#   subdomains thereof, except addresses with sender-specified routing.
# The default relay_domains value is $mydestination.
# 
# In addition to the above, the Postfix SMTP server by default accepts mail
# that Postfix is final destination for:
# - destinations that match $inet_interfaces or $proxy_interfaces,
# - destinations that match $mydestination
# - destinations that match $virtual_alias_domains,
# - destinations that match $virtual_mailbox_domains.
# These destinations do not need to be listed in $relay_domains.
# 
# Specify a list of hosts or domains, /file/name patterns or type:name
# lookup tables, separated by commas and/or whitespace.  Continue
# long lines by starting the next line with whitespace. A file name
# is replaced by its contents; a type:name table is matched when a
# (parent) domain appears as lookup key.
#
# NOTE: Postfix will not automatically forward mail for domains that
# list this system as their primary or backup MX host. See the
# permit_mx_backup restriction description in postconf(5).
#
relay_domains = $mydestination

# INTERNET OR INTRANET

# The relayhost parameter specifies the default host to send mail to
# when no entry is matched in the optional transport(5) table. When
# no relayhost is given, mail is routed directly to the destination.
#
# On an intranet, specify the organizational domain name. If your
# internal DNS uses no MX records, specify the name of the intranet
# gateway host instead.
#
# In the case of SMTP, specify a domain, host, host:port, [host]:port,
# [address] or [address]:port; the form [host] turns off MX lookups.
#
# If you're connected via UUCP, see also the default_transport parameter.
#
#relayhost = $mydomain
#relayhost = [gateway.my.domain]
#relayhost = [mailserver.isp.tld]
#relayhost = uucphost
#relayhost = [an.ip.add.ress]

# REJECTING UNKNOWN RELAY USERS
#
# The relay_recipient_maps parameter specifies optional lookup tables
# with all addresses in the domains that match $relay_domains.
#
# If this parameter is defined, then the SMTP server will reject
# mail for unknown relay users. This feature is off by default.
#
# The right-hand side of the lookup tables is conveniently ignored.
# In the left-hand side, specify an @domain.tld wild-card, or specify
# a user@domain.tld address.
# 
#relay_recipient_maps = hash:/etc/postfix/relay_recipients

# INPUT RATE CONTROL
#
# The in_flow_delay configuration parameter implements mail input
# flow control. This feature is turned on by default, although it
# still needs further development (it's disabled on SCO UNIX due
# to an SCO bug).
# 
# A Postfix process will pause for $in_flow_delay seconds before
# accepting a new message, when the message arrival rate exceeds the
# message delivery rate. With the default 100 SMTP server process
# limit, this limits the mail inflow to 100 messages a second more
# than the number of messages delivered per second.
# 
# Specify 0 to disable the feature. Valid delays are 0..10.
# 
#in_flow_delay = 1s

# ADDRESS REWRITING
#
# The ADDRESS_REWRITING_README document gives information about
# address masquerading or other forms of address rewriting including
# username->Firstname.Lastname mapping.

# ADDRESS REDIRECTION (VIRTUAL DOMAIN)
#
# The VIRTUAL_README document gives information about the many forms
# of domain hosting that Postfix supports.

# "USER HAS MOVED" BOUNCE MESSAGES
#
# See the discussion in the ADDRESS_REWRITING_README document.

# TRANSPORT MAP
#
# See the discussion in the ADDRESS_REWRITING_README document.

# ALIAS DATABASE
#
# The alias_maps parameter specifies the list of alias databases used
# by the local delivery agent. The default list is system dependent.
#
# On systems with NIS, the default is to search the local alias
# database, then the NIS alias database. See aliases(5) for syntax
# details.
# 
# If you change the alias database, run "postalias /etc/aliases" (or
# wherever your system stores the mail alias file), or simply run
# "newaliases" to build the necessary DBM or DB file.
#
# It will take a minute or so before changes become visible.  Use
# "postfix reload" to eliminate the delay.
#
#alias_maps = dbm:/etc/aliases
alias_maps = hash:/etc/aliases
#alias_maps = hash:/etc/aliases, nis:mail.aliases
#alias_maps = netinfo:/aliases

# The alias_database parameter specifies the alias database(s) that
# are built with "newaliases" or "sendmail -bi".  This is a separate
# configuration parameter, because alias_maps (see above) may specify
# tables that are not necessarily all under control by Postfix.
#
#alias_database = dbm:/etc/aliases
#alias_database = dbm:/etc/mail/aliases
alias_database = hash:/etc/aliases
#alias_database = hash:/etc/aliases, hash:/opt/majordomo/aliases

# ADDRESS EXTENSIONS (e.g., user+foo)
#
# The recipient_delimiter parameter specifies the separator between
# user names and address extensions (user+foo). See canonical(5),
# local(8), relocated(5) and virtual(5) for the effects this has on
# aliases, canonical, virtual, relocated and .forward file lookups.
# Basically, the software tries user+foo and .forward+foo before
# trying user and .forward.
#
#recipient_delimiter = +

# DELIVERY TO MAILBOX
#
# The home_mailbox parameter specifies the optional pathname of a
# mailbox file relative to a user's home directory. The default
# mailbox file is /var/spool/mail/user or /var/mail/user.  Specify
# "Maildir/" for qmail-style delivery (the / is required).
#
#home_mailbox = Mailbox
#home_mailbox = Maildir/
 
# The mail_spool_directory parameter specifies the directory where
# UNIX-style mailboxes are kept. The default setting depends on the
# system type.
#
#mail_spool_directory = /var/mail
#mail_spool_directory = /var/spool/mail

# The mailbox_command parameter specifies the optional external
# command to use instead of mailbox delivery. The command is run as
# the recipient with proper HOME, SHELL and LOGNAME environment settings.
# Exception:  delivery for root is done as $default_user.
#
# Other environment variables of interest: USER (recipient username),
# EXTENSION (address extension), DOMAIN (domain part of address),
# and LOCAL (the address localpart).
#
# Unlike other Postfix configuration parameters, the mailbox_command
# parameter is not subjected to $parameter substitutions. This is to
# make it easier to specify shell syntax (see example below).
#
# Avoid shell meta characters because they will force Postfix to run
# an expensive shell process. Procmail alone is expensive enough.
#
# IF YOU USE THIS TO DELIVER MAIL SYSTEM-WIDE, YOU MUST SET UP AN
# ALIAS THAT FORWARDS MAIL FOR ROOT TO A REAL USER.
#
#mailbox_command = /some/where/procmail
#mailbox_command = /some/where/procmail -a "$EXTENSION"

# The mailbox_transport specifies the optional transport in master.cf
# to use after processing aliases and .forward files. This parameter
# has precedence over the mailbox_command, fallback_transport and
# luser_relay parameters.
#
# Specify a string of the form transport:nexthop, where transport is
# the name of a mail delivery transport defined in master.cf.  The
# :nexthop part is optional. For more details see the sample transport
# configuration file.
#
# NOTE: if you use this feature for accounts not in the UNIX password
# file, then you must update the "local_recipient_maps" setting in
# the main.cf file, otherwise the SMTP server will reject mail for    
# non-UNIX accounts with "User unknown in local recipient table".
#
#mailbox_transport = lmtp:unix:/var/lib/imap/socket/lmtp

# If using the cyrus-imapd IMAP server deliver local mail to the IMAP
# server using LMTP (Local Mail Transport Protocol), this is prefered
# over the older cyrus deliver program by setting the
# mailbox_transport as below:
#
# mailbox_transport = lmtp:unix:/var/lib/imap/socket/lmtp
#
# The efficiency of LMTP delivery for cyrus-imapd can be enhanced via
# these settings.
#
# local_destination_recipient_limit = 300
# local_destination_concurrency_limit = 5
#
# Of course you should adjust these settings as appropriate for the
# capacity of the hardware you are using. The recipient limit setting
# can be used to take advantage of the single instance message store
# capability of Cyrus. The concurrency limit can be used to control
# how many simultaneous LMTP sessions will be permitted to the Cyrus
# message store. 
#
# To use the old cyrus deliver program you have to set:
#mailbox_transport = cyrus

# The fallback_transport specifies the optional transport in master.cf
# to use for recipients that are not found in the UNIX passwd database.
# This parameter has precedence over the luser_relay parameter.
#
# Specify a string of the form transport:nexthop, where transport is
# the name of a mail delivery transport defined in master.cf.  The
# :nexthop part is optional. For more details see the sample transport
# configuration file.
#
# NOTE: if you use this feature for accounts not in the UNIX password
# file, then you must update the "local_recipient_maps" setting in
# the main.cf file, otherwise the SMTP server will reject mail for    
# non-UNIX accounts with "User unknown in local recipient table".
#
#fallback_transport = lmtp:unix:/var/lib/imap/socket/lmtp
#fallback_transport =

# The luser_relay parameter specifies an optional destination address
# for unknown recipients.  By default, mail for unknown@$mydestination,
# unknown@[$inet_interfaces] or unknown@[$proxy_interfaces] is returned
# as undeliverable.
#
# The following expansions are done on luser_relay: $user (recipient
# username), $shell (recipient shell), $home (recipient home directory),
# $recipient (full recipient address), $extension (recipient address
# extension), $domain (recipient domain), $local (entire recipient
# localpart), $recipient_delimiter. Specify ${name?value} or
# ${name:value} to expand value only when $name does (does not) exist.
#
# luser_relay works only for the default Postfix local delivery agent.
#
# NOTE: if you use this feature for accounts not in the UNIX password
# file, then you must specify "local_recipient_maps =" (i.e. empty) in
# the main.cf file, otherwise the SMTP server will reject mail for    
# non-UNIX accounts with "User unknown in local recipient table".
#
#luser_relay = $user@other.host
#luser_relay = $local@other.host
#luser_relay = admin+$local
  
# JUNK MAIL CONTROLS
# 
# The controls listed here are only a very small subset. The file
# SMTPD_ACCESS_README provides an overview.

# The header_checks parameter specifies an optional table with patterns
# that each logical message header is matched against, including
# headers that span multiple physical lines.
#
# By default, these patterns also apply to MIME headers and to the
# headers of attached messages. With older Postfix versions, MIME and
# attached message headers were treated as body text.
#
# For details, see "man header_checks".
#
#header_checks = regexp:/etc/postfix/header_checks

# FAST ETRN SERVICE
#
# Postfix maintains per-destination logfiles with information about
# deferred mail, so that mail can be flushed quickly with the SMTP
# "ETRN domain.tld" command, or by executing "sendmail -qRdomain.tld".
# See the ETRN_README document for a detailed description.
# 
# The fast_flush_domains parameter controls what destinations are
# eligible for this service. By default, they are all domains that
# this server is willing to relay mail to.
# 
#fast_flush_domains = $relay_domains

# SHOW SOFTWARE VERSION OR NOT
#
# The smtpd_banner parameter specifies the text that follows the 220
# code in the SMTP server's greeting banner. Some people like to see
# the mail version advertised. By default, Postfix shows no version.
#
# You MUST specify $myhostname at the start of the text. That is an
# RFC requirement. Postfix itself does not care.
#
#smtpd_banner = $myhostname ESMTP $mail_name
#smtpd_banner = $myhostname ESMTP $mail_name ($mail_version)

# PARALLEL DELIVERY TO THE SAME DESTINATION
#
# How many parallel deliveries to the same user or domain? With local
# delivery, it does not make sense to do massively parallel delivery
# to the same user, because mailbox updates must happen sequentially,
# and expensive pipelines in .forward files can cause disasters when
# too many are run at the same time. With SMTP deliveries, 10
# simultaneous connections to the same domain could be sufficient to
# raise eyebrows.
# 
# Each message delivery transport has its XXX_destination_concurrency_limit
# parameter.  The default is $default_destination_concurrency_limit for
# most delivery transports. For the local delivery agent the default is 2.

#local_destination_concurrency_limit = 2
#default_destination_concurrency_limit = 20

# DEBUGGING CONTROL
#
# The debug_peer_level parameter specifies the increment in verbose
# logging level when an SMTP client or server host name or address
# matches a pattern in the debug_peer_list parameter.
#
debug_peer_level = 2

# The debug_peer_list parameter specifies an optional list of domain
# or network patterns, /file/name patterns or type:name tables. When
# an SMTP client or server host name or address matches a pattern,
# increase the verbose logging level by the amount specified in the
# debug_peer_level parameter.
#
#debug_peer_list = 127.0.0.1
#debug_peer_list = some.domain

# The debugger_command specifies the external command that is executed
# when a Postfix daemon program is run with the -D option.
#
# Use "command .. & sleep 5" so that the debugger can attach before
# the process marches on. If you use an X-based debugger, be sure to
# set up your XAUTHORITY environment variable before starting Postfix.
#
debugger_command =
	 PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
	 ddd $daemon_directory/$process_name $process_id & sleep 5

# If you can't use X, use this to capture the call stack when a
# daemon crashes. The result is in a file in the configuration
# directory, and is named after the process name and the process ID.
#
# debugger_command =
#	PATH=/bin:/usr/bin:/usr/local/bin; export PATH; (echo cont;
#	echo where) | gdb $daemon_directory/$process_name $process_id 2>&1
#	>$config_directory/$process_name.$process_id.log & sleep 5
#
# Another possibility is to run gdb under a detached screen session.
# To attach to the screen sesssion, su root and run "screen -r
# <id_string>" where <id_string> uniquely matches one of the detached
# sessions (from "screen -list").
#
# debugger_command =
#	PATH=/bin:/usr/bin:/sbin:/usr/sbin; export PATH; screen
#	-dmS $process_name gdb $daemon_directory/$process_name
#	$process_id & sleep 1

# INSTALL-TIME CONFIGURATION INFORMATION
#
# The following parameters are used when installing a new Postfix version.
# 
# sendmail_path: The full pathname of the Postfix sendmail command.
# This is the Sendmail-compatible mail posting interface.
# 
sendmail_path = /usr/sbin/sendmail.postfix

# newaliases_path: The full pathname of the Postfix newaliases command.
# This is the Sendmail-compatible command to build alias databases.
#
newaliases_path = /usr/bin/newaliases.postfix

# mailq_path: The full pathname of the Postfix mailq command.  This
# is the Sendmail-compatible mail queue listing command.
# 
mailq_path = /usr/bin/mailq.postfix

# setgid_group: The group for mail submission and queue management
# commands.  This must be a group name with a numerical group ID that
# is not shared with other accounts, not even with the Postfix account.
#
setgid_group = postdrop

# html_directory: The location of the Postfix HTML documentation.
#
html_directory = no

# manpage_directory: The location of the Postfix on-line manual pages.
#
manpage_directory = /usr/share/man

# sample_directory: The location of the Postfix sample configuration files.
# This parameter is obsolete as of Postfix 2.1.
#
sample_directory = /usr/share/doc/postfix-2.6.6/samples

# readme_directory: The location of the Postfix README files.
#
readme_directory = /usr/share/doc/postfix-2.6.6/README_FILES
    """
    dovecot_config = """
## Dovecot configuration file

# If you're in a hurry, see http://wiki.dovecot.org/QuickConfiguration

# "doveconf -n" command gives a clean output of the changed settings. Use it
# instead of copy&pasting files when posting to the Dovecot mailing list.

# '#' character and everything after it is treated as comments. Extra spaces
# and tabs are ignored. If you want to use either of these explicitly, put the
# value inside quotes, eg.: key = "# char and trailing whitespace  "

# Default values are shown for each setting, it's not required to uncomment
# those. These are exceptions to this though: No sections (e.g. namespace {})
# or plugin settings are added by default, they're listed only as examples.
# Paths are also just examples with the real defaults being based on configure
# options. The paths listed here are for configure --prefix=/usr
# --sysconfdir=/etc --localstatedir=/var

# Protocols we want to be serving.
protocols = imap imaps pop3 pop3s

# A comma separated list of IPs or hosts where to listen in for connections. 
# "*" listens in all IPv4 interfaces, "::" listens in all IPv6 interfaces.
# If you want to specify non-default ports or anything more complex,
# edit conf.d/master.conf.
listen = *, ::

# Base directory where to store runtime data.
#base_dir = /var/run/dovecot/

# Greeting message for clients.
#login_greeting = Dovecot ready.

# Space separated list of trusted network ranges. Connections from these
# IPs are allowed to override their IP addresses and ports (for logging and
# for authentication checks). disable_plaintext_auth is also ignored for
# these networks. Typically you'd specify your IMAP proxy servers here.
#login_trusted_networks =

# Sepace separated list of login access check sockets (e.g. tcpwrap)
#login_access_sockets = 

# Show more verbose process titles (in ps). Currently shows user name and
# IP address. Useful for seeing who are actually using the IMAP processes
# (eg. shared mailboxes or if same uid is used for multiple accounts).
#verbose_proctitle = no

# Should all processes be killed when Dovecot master process shuts down.
# Setting this to "no" means that Dovecot can be upgraded without
# forcing existing client connections to close (although that could also be
# a problem if the upgrade is e.g. because of a security fix).
#shutdown_clients = yes

# If non-zero, run mail commands via this many connections to doveadm server,
# instead of running them directly in the same process.
#doveadm_worker_count = 0
# UNIX socket or host:port used for connecting to doveadm server
#doveadm_socket_path = doveadm-server

##
## Dictionary server settings
##

# Dictionary can be used to store key=value lists. This is used by several
# plugins. The dictionary can be accessed either directly or though a
# dictionary server. The following dict block maps dictionary names to URIs
# when the server is used. These can then be referenced using URIs in format
# "proxy::<name>".

dict {
  #quota = mysql:/etc/dovecot/dovecot-dict-sql.conf.ext
  #expire = sqlite:/etc/dovecot/dovecot-dict-sql.conf.ext
}

# Most of the actual configuration gets included below. The filenames are
# first sorted by their ASCII value and parsed in that order. The 00-prefixes
# in filenames are intended to make it easier to understand the ordering.
!include conf.d/*.conf

# A config file can also tried to be included without giving an error if
# it's not found:
#!include_try /etc/dovecot/local.conf
    """
    f = open("/etc/postfix/main.cf","w+")
    f.write(main_config)
    f.close()
    f = open("/etc/dovecot/dovecot.conf","w+")
    f.write(dovecot_config)
    f.close()
    #os.system("postconf -e mailbox_size_limit=" + str(mailbox_size*1024*1000))
    #os.system("postconf -e message_size_limit=" + str(message_size*1024*1000))
    Service('dovecot','restart')
    Service('postfix','restart')

def PXE_Server(dhcp_domain, dhcp_network, dhcp_netmask, dhcp_netrange, dns_domain, dns_addr, default_router, min_release, max_release, pxe_nexttop, tftp_boot_root, ftp_root):
    os.system("yum install dhcp -y; yum install xinetd -y; yum install tftp-server -y ; yum install syslinux -y ; yum install vsftpd -y")
    if not os.path.exists(tftp_boot_root):
        os.system("mkdir " + tftp_boot_root)
        os.system("chmod 777 " + tftp_boot_root)
    if not os.path.exists(ftp_root):
        os.system("mkdir " + ftp_root)
        os.system("chmod 777 " + ftp_root)
    dhcp_config = '''
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.sample
#   see 'man 5 dhcpd.conf'
#
shared-network ''' + dhcp_domain + ''' {
subnet ''' + dhcp_network + ''' netmask ''' + dhcp_netmask + ''' {
  range ''' + dhcp_netrange + ''';
  option domain-name-servers ''' + dns_addr + ''';
''' + '''
  option domain-name "''' + dns_domain + '''";
  option routers ''' + default_router + ''';
  default-lease-time ''' + min_release + ''';
  max-lease-time ''' + max_release + ''';
  next-server ''' + pxe_nexttop + ''';
  filename "pxelinux.0";
}
}
'''
    f = open("/etc/dhcp/dhcpd.conf","w+")
    f.write(dhcp_config)
    f.close()
    tftp_config = """
# default: off
# description: The tftp server serves files using the trivial file transfer \
#	protocol.  The tftp protocol is often used to boot diskless \
#	workstations, download configuration files to network-aware printers, \
#	and to start the installation process for some operating systems.
service tftp
{
	socket_type		= dgram
	protocol		= udp
	wait			= yes
	user			= root
	server			= /usr/sbin/in.tftpd
	server_args		= -s """ + tftp_boot_root + """
	disable			= no
	per_source		= 11
	cps			= 100 2
	flags			= IPv4
}
"""
    f = open("/etc/xinetd.d/tftp","w+")
    f.write(tftp_config)
    f.close()
    os.system("cp /mnt/src/isolinux/* " + tftp_boot_root + "/ -r")
    os.system("cp /usr/share/syslinux/pxelinux.0 " + tftp_boot_root + "/")
    os.system("mkdir " + tftp_boot_root + "/pxelinux.cfg ; cp " + tftp_boot_root  + "/isolinux.cfg " + tftp_boot_root + "/pxelinux.cfg/default")
    Service('dhcpd','restart')
    Service('xinetd','restart')
    Service('vsftpd','restart')
    os.system("setenforce 0")
    os.system("cp /mnt/src/* " + ftp_root + "/ -r")

def bind_configure(hostname='dns', domain_name='zeronet.club', arpa_area='0.0.0.0'):
    os.system("yum install bind -y")
    Sour_Bind_IN_List = """
ns	    IN	A	10.10.10.244
node1	IN	A	10.10.10.245
node2	IN	A	10.10.10.246
node3	IN	A	10.10.10.250
"""
    Sour_Bind_Arpa_List = """
ns	    IN	A	10.10.10.244
244	IN	PTR	ns.zeronet.club
245	IN	PTR	node1.zeronet.club
246	IN	PTR	node2.zeronet.club
250	IN	PTR	node3.zeronet.club
"""
    with open("/etc/named.inlist", "w+") as f:
        f.write(Sour_Bind_IN_List)
    with open("/etc/named.arpalist", "w+") as f:
        f.write(Sour_Bind_Arpa_List)
    os.system(edit + " /etc/named.inlist")
    os.system(edit + " /etc/named.arpalist")
    with open("/etc/named.inlist", "r") as f:
        Bind_IN_List = f.read()
    with open("/etc/named.arpalist", "r") as f:
        Bind_Arpa_List = f.read()
    bind_config = """
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
	listen-on port 53 { any; };
	listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
	allow-query     { any; };
	recursion yes;

	dnssec-enable yes;
	dnssec-validation yes;
	dnssec-lookaside auto;

	/* Path to ISC DLV key */
	bindkeys-file "/etc/named.iscdlv.key";

	managed-keys-directory "/var/named/dynamic";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
	type hint;
	file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

"""
    f = open("/etc/named.conf","w+")
    f.write(bind_config)
    f.close()

    main_config = """
// named.rfc1912.zones:
//
// Provided by Red Hat caching-nameserver package 
//
// ISC BIND named zone configuration for zones recommended by
// RFC 1912 section 4.1 : localhost TLDs and address zones
// and http://www.ietf.org/internet-drafts/draft-ietf-dnsop-default-local-zones-02.txt
// (c)2007 R W Franks
// 
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

zone "localhost.localdomain" IN {
	type master;
	file "named.localhost";
	allow-update { none; };
};

zone "localhost" IN {
	type master;
	file "named.localhost";
	allow-update { none; };
};

zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
	type master;
	file "named.loopback";
	allow-update { none; };
};

zone "1.0.0.127.in-addr.arpa" IN {
	type master;
	file "named.loopback";
	allow-update { none; };
};

zone "0.in-addr.arpa" IN {
	type master;
	file "named.empty";
	allow-update { none; };
};

""" + '''
zone "''' + domain_name + '''" IN {
	type master;
	file "new.in";
	allow-update { none; };
};

zone "''' + arpa_area + '''.in-addr.arpa" IN {
	type master;
	file "new.arpa";
	allow-update { none; };
};
'''
    f = open("/etc/named.rfc1912.zones","w+")
    f.write(main_config)
    f.close()
    new_in_config = """
$TTL 1D
@	IN SOA	""" + domain_name + """. rname.invalid. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
        NS      @
        A       127.0.0.1
        AAAA    ::1
""" + Bind_IN_List

    new_arpa_config = """
$TTL 1D
@	IN SOA	""" + domain_name + """. rname.invalid. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
	IN	NS	@
	A	127.0.0.1
	AAAA	::1
	PTR	localhost.
""" + Bind_Arpa_List
    f = open("/var/named/new.in","w+")
    f.write(new_in_config)
    f.close()
    f = open("/var/named/new.arpa","w+")
    f.write(new_arpa_config)
    f.close()
    os.system("chmod 640 /var/named/new.in ; chmod 640 /var/named/new.arpa")
    Service('named','restart')

def nis_configure(nisdomain):
    Commands_List = ['yum install portmap ypserv ypbind yp-tools -y ',
    'nisdomainname ' + nisdomain,
    'echo "/bin/nisdomainname ' + nisdomain + '" >>/etc/rc.d/rc.local',
    'echo "NISDOMAIN=' + nisdomain + '" >> /etc/sysconfig/network']
    Sour_NIS_ACL = """
# NIS ACL Example :
127.0.0.0/255.0.0.0     :  *  :  *  :  none 
100.0.0.0/255.0.0.0     :  *  :  *  :  none 
*                       :  *  :  *  :  deny
"""
    with open("/etc/ypserv.acl","w+") as f:
        f.write(Sour_NIS_ACL)
    os.system(edit + " /etc/ypserv.acl")
    with open("/etc/ypserv.acl","r") as f:
        NIS_ACL = f.read()
    NIS_Config = """
#
# ypserv.conf	In this file you can set certain options for the NIS server,
#		and you can deny or restrict access to certain maps based
#		on the originating host.
#
#		See ypserv.conf(5) for a description of the syntax.
#

# Some options for ypserv. This things are all not needed, if
# you have a Linux net.

# Should we do DNS lookups for hosts not found in the hosts table ?
# This option is ignored in the moment.
dns: no

# How many map file handles should be cached ?
files: 30

# Should we register ypserv with SLP ?
# slp: no
# After how many seconds we should re-register ypserv with SLP ?
# slp_timeout: 3600

# xfr requests are only allowed from ports < 1024
xfr_check_port: yes

# The following, when uncommented,  will give you shadow like passwords.
# Note that it will not work if you have slave NIS servers in your
# network that do not run the same server as you.

# Host                     : Domain  : Map              : Security 
#
# *                        : *       : passwd.byname    : port 
# *                        : *       : passwd.byuid     : port

# Not everybody should see the shadow passwords, not secure, since
# under MSDOG everbody is root and can access ports < 1024 !!!
*			   : *       : shadow.byname    : port
*			   : *       : passwd.adjunct.byname : port

# If you comment out the next rule, ypserv and rpc.ypxfrd will
# look for YP_SECURE and YP_AUTHDES in the maps. This will make
# the security check a little bit slower, but you only have to
# change the keys on the master server, not the configuration files
# on each NIS server.
# If you have maps with YP_SECURE or YP_AUTHDES, you should create
# a rule for them above, that's much faster.
""" + NIS_ACL
    with open("/etc/ypserv.conf","w+") as f:
        f.write(NIS_Config)
    os.system("echo NIS service need create new user if not create please input 'ml' to jmp it.")
    while 1:
        nisusername = raw_input("Add Username : ")
        if nisusername == "ml":
            break
        else:
            os.system("useradd " + str(nisusername))
            os.system("passwd " + str(nisusername))
    for cmd in Commands_List:
        os.system(cmd)
    Service("rpcbind",'restart')
    Service("ypserv",'restart')
    Auto_Enable('rpcbind','on')
    Auto_Enable('ypserv','on')
    os.system("echo 'Ctrl+D' to jmp add host step.")
    os.system("/usr/lib64/yp/ypinit -m")

def ftp_configure(Virtual_UserName='admin', Virtual_Path='/home/admin', Virtual_User_Conf='/etc/vsftpd/vsftpd_user_config_dir', Ftp_Path='/var/ftpsite', SSL_Enable='no'):
    os.system('yum install vsftpd -y')
    os.system('yum install ftp -y')
    os.system('yum install db4')
    if SSL_Enable == "yes":
        ssl_status = """
# ssl or tls 
ssl_enable=YES
ssl_sslv3=YES
ssl_tlsv1=YES
allow_anon_ssl=NO
force_local_data_ssl=YES
force_local_logins_ssl=YES
rsa_cert_file=/etc/vsftpd/vsftpd.crt
rsa_private_key_file=/etc/vsftpd/vsftpd.key
"""
    else:
        ssl_status = ""
    vsftp_config = """
local_umask=022
connect_from_port_20=NO
use_localtime=YES
listen=YES
userlist_enable=YES
local_enable=YES
write_enable=YES
dirmessage_enable=YES
xferlog_enable=YES
#chown_uploads=YES
#chown_username=whoever
xferlog_file=/var/log/xferlog
xferlog_std_format=YES
#idle_session_timeout=600
#data_connection_timeout=120
#nopriv_user=ftpsecure
#async_abor_enable=YES
#ascii_upload_enable=YES
#ascii_download_enable=YES
#deny_email_enable=YES
#chroot_local_user=YES
#chroot_list_enable=YES
# (default follows)
#chroot_list_file=/etc/vsftpd/chroot_list
#ls_recurse_enable=YES
#listen_ipv6=YES
tcp_wrappers=YES

pam_service_name=vsftpd
pasv_enable=YES
pasv_min_port=10030
pasv_max_port=10035
local_enable=YES
anonymous_enable=YES
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
guest_enable=YES
guest_username=""" + Virtual_UserName + """
user_config_dir=""" + Virtual_User_Conf + """
local_root=""" + Ftp_Path + """
anon_root=""" + Ftp_Path + """
""" + ssl_status
    vsftpd_user_config = """
local_root=""" + Ftp_Path + """
anon_root=""" + Ftp_Path + """
write_enable=YES
anon_world_readable_only=YES
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
"""
    Commands_List = ['mkdir ' + Virtual_Path,
    'echo Setting Main Virtual User.',
    'useradd ' + Virtual_UserName  + ' -s /sbin/nologin',
    'echo Setting Main Virtual User Password.',
    'passwd ' + Virtual_UserName,
    'chmod 777 /home/' + Virtual_UserName,
    'echo user1 >>/etc/vsftpd/users_list',
    'echo user1pass >>/etc/vsftpd/users_list',
    'echo Setting vsftpd userlist, because vsftpd use pam.d to authentication.',
    edit + ' /etc/vsftpd/users_list',
    'db_load -T -t hash -f /etc/vsftpd/users_list /etc/vsftpd/users.db',
    'chmod 600 /etc/vsftpd/* -R',
    'chmod 755 ' + Virtual_Path  + ' -R',
    'mkdir ' + Virtual_User_Conf,
    'mkdir ' + Ftp_Path,
    'chmod 777 ' + Ftp_Path]
    for cmd in Commands_List:
        os.system(cmd)
    os.system("echo The Vsftpd service need create new user if not create please input 'ml' to jmp it.")
    while 1:
        ftpusername = raw_input("Add Username : ")
        if ftpusername == "ml":
            break
        else:
            os.system("useradd -d " + Virtual_Path + " " + str(ftpusername) + " -s /sbin/nologin")
            os.system("passwd " + str(ftpusername))
            with open(Virtual_User_Conf + '/' + ftpusername, "w+") as f:
                f.write(vsftpd_user_config)
            os.system(edit + Virtual_User_Conf + '/' + ftpusername)
    with open("/etc/vsftpd/vsftpd.conf","w+") as f:
        f.write(vsftp_config)
    os.system("chmod 777 /etc/vsftpd -R")
    os.system("chmod 777 /etc/pam.d -R")
    os.system("chmod 664 /etc/vsftpd/ftpusers")
    if SSL_Enable == "yes":
        os.system("cd /etc/ssl/certs/ ; make vsftpd.crt ; cp ./vsftpd.crt /etc/vsftpd/ ; cp ./vsftpd.key /etc/vsftpd/")
    Service("vsftpd","restart")
    Auto_Enable("vsftpd","on")

def sendmail_configure(MaxMessageSize, hostname):
    Commands_List = ['yum install cyrus-sasl -y',
    'yum install cyrus-sasl-md5 -y',
    'yum install cyrus-sasl-ntlm -y',
    'yum install cyrus-sasl-sql -y',
    'yum install cyrus-sasl-gssapi -y',
    'yum install sendmail -y']
    for cmd in Commands_List:
        os.system(cmd)
    os.system("echo [+] Starting Sendmail ... But you need change your hostname. Please input your new hostname. Example: 'abc.com'")
    if OS_V == 'C6':
        os.system('hostname ' + hostname)
    else:
        os.system('hostnamectl set-hostname ' + hostname)
    os.system("echo " + hostname + ">/etc/mail/local-host-names")
    Access_config = """
# Check the /usr/share/doc/sendmail/README.cf file for a description
# of the format of this file. (search for access_db in that file)
# The /usr/share/doc/sendmail/README.cf is part of the sendmail-doc
# package.
#
# If you want to use AuthInfo with "M:PLAIN LOGIN", make sure to have the 
# cyrus-sasl-plain package installed.
#
# By default we allow relaying from localhost...
Connect:localhost.localdomain		RELAY
Connect:localhost			RELAY
Connect:127.0.0.1			RELAY

Connect:0.0.0.0 			OK
                            RELAY
                            REJECT
                            DISCARD
"""
    with open("/etc/mail/access","w+") as f:
        f.write(Access_config)
    os.system(edit + " /etc/mail/access ; cd /etc/mail/ ; makemap hash access.db < access")
    os.system("echo [+] Maybe you need to setting aliases...")
    os.system(edit + " /etc/aliases")
    sendmail_config = '''
#
# Copyright (c) 1998-2004, 2009 Sendmail, Inc. and its suppliers.
#	All rights reserved.
# Copyright (c) 1983, 1995 Eric P. Allman.  All rights reserved.
# Copyright (c) 1988, 1993
#	The Regents of the University of California.  All rights reserved.
#
# By using this file, you agree to the terms and conditions set
# forth in the LICENSE file which can be found at the top level of
# the sendmail distribution.
#
#

######################################################################
######################################################################
#####
#####		SENDMAIL CONFIGURATION FILE
#####
##### built by root@192.168.145.130 on Sun Feb 24 19:06:42 PST 2019
##### in /etc/mail
##### using /usr/share/sendmail-cf/ as configuration include directory
#####
######################################################################
#####
#####	DO NOT EDIT THIS FILE!  Only edit the source .mc file.
#####
######################################################################
######################################################################

#####  $Id: cfhead.m4,v 8.120 2009/01/23 22:39:21 ca Exp $  #####
#####  $Id: cf.m4,v 8.32 1999/02/07 07:26:14 gshapiro Exp $  #####
#####  setup for linux  #####
#####  $Id: linux.m4,v 8.13 2000/09/17 17:30:00 gshapiro Exp $  #####



#####  $Id: local_procmail.m4,v 8.22 2002/11/17 04:24:19 ca Exp $  #####


#####  $Id: no_default_msa.m4,v 8.2 2001/02/14 05:03:22 gshapiro Exp $  #####

#####  $Id: smrsh.m4,v 8.14 1999/11/18 05:06:23 ca Exp $  #####

#####  $Id: mailertable.m4,v 8.25 2002/06/27 23:23:57 gshapiro Exp $  #####

#####  $Id: virtusertable.m4,v 8.23 2002/06/27 23:23:57 gshapiro Exp $  #####

#####  $Id: redirect.m4,v 8.15 1999/08/06 01:47:36 gshapiro Exp $  #####

#####  $Id: always_add_domain.m4,v 8.11 2000/09/12 22:00:53 ca Exp $  #####

#####  $Id: use_cw_file.m4,v 8.11 2001/08/26 20:58:57 gshapiro Exp $  #####


#####  $Id: use_ct_file.m4,v 8.11 2001/08/26 20:58:57 gshapiro Exp $  #####


#####  $Id: local_procmail.m4,v 8.22 2002/11/17 04:24:19 ca Exp $  #####

#####  $Id: access_db.m4,v 8.27 2006/07/06 21:10:10 ca Exp $  #####

#####  $Id: blacklist_recipients.m4,v 8.13 1999/04/02 02:25:13 gshapiro Exp $  #####

#####  $Id: accept_unresolvable_domains.m4,v 8.10 1999/02/07 07:26:07 gshapiro Exp $  #####


#####  $Id: proto.m4,v 8.741 2009/12/11 00:04:53 ca Exp $  #####

# level 10 config file format
V10/Berkeley

# override file safeties - setting this option compromises system security,
# addressing the actual file configuration problem is preferred
# need to set this before any file actions are encountered in the cf file
#O DontBlameSendmail=safe

# default LDAP map specification
# need to set this now before any LDAP maps are defined
#O LDAPDefaultSpec=-h localhost

##################
#   local info   #
##################

# my LDAP cluster
# need to set this before any LDAP lookups are done (including classes)
#D{sendmailMTACluster}$m

Cwlocalhost
# file containing names of hosts for which we receive email
Fw/etc/mail/local-host-names

# my official domain name
# ... define this only if sendmail cannot automatically determine your domain
#Dj$w.Foo.COM

# host/domain names ending with a token in class P are canonical
CP.

# "Smart" relay host (may be null)
DS


# operators that cannot be in local usernames (i.e., network indicators)
CO @ % !

# a class with just dot (for identifying canonical names)
C..

# a class with just a left bracket (for identifying domain literals)
C[[

# access_db acceptance class
C{Accept}OK RELAY


C{ResOk}OKR


# Hosts for which relaying is permitted ($=R)
FR-o /etc/mail/relay-domains

# arithmetic map
Karith arith
# macro storage map
Kmacro macro
# possible values for TLS_connection in access map
C{Tls}VERIFY ENCR





# dequoting map
Kdequote dequote

# class E: names that should be exposed as from this host, even if we masquerade
# class L: names that should be delivered locally, even if we have a relay
# class M: domains that should be converted to $M
# class N: domains that should not be converted to $M
#CL root
C{E}root
C{w}localhost.localdomain



# my name for error messages
DnMAILER-DAEMON


# Mailer table (overriding domains)
Kmailertable hash -o /etc/mail/mailertable.db

# Virtual user table (maps incoming users)
Kvirtuser hash -o /etc/mail/virtusertable.db

CPREDIRECT

# Access list database (for spam stomping)
Kaccess hash -T<TMPF> -o /etc/mail/access.db

# Configuration version number
DZ8.14.4


###############
#   Options   #
###############

# strip message body to 7 bits on input?
O SevenBitInput=False

# 8-bit data handling
#O EightBitMode=pass8

# wait for alias file rebuild (default units: minutes)
O AliasWait=10

# location of alias file
O AliasFile=/etc/aliases

# minimum number of free blocks on filesystem
O MinFreeBlocks=100

# maximum message size
O MaxMessageSize=""" + str(MaxMessageSize *1024 *1000)"""

# substitution for space (blank) characters
O BlankSub=.

# avoid connecting to "expensive" mailers on initial submission?
O HoldExpensive=False

# checkpoint queue runs after every N successful deliveries
#O CheckpointInterval=10

# default delivery mode
O DeliveryMode=background

# error message header/file
#O ErrorHeader=/etc/mail/error-header

# error mode
#O ErrorMode=print

# save Unix-style "From_" lines at top of header?
#O SaveFromLine=False

# queue file mode (qf files)
#O QueueFileMode=0600

# temporary file mode
O TempFileMode=0600

# match recipients against GECOS field?
#O MatchGECOS=False

# maximum hop count
#O MaxHopCount=25

# location of help file
O HelpFile=/etc/mail/helpfile

# ignore dots as terminators in incoming messages?
#O IgnoreDots=False

# name resolver options
#O ResolverOptions=+AAONLY

# deliver MIME-encapsulated error messages?
O SendMimeErrors=True

# Forward file search path
O ForwardPath=$z/.forward.$w:$z/.forward

# open connection cache size
O ConnectionCacheSize=2

# open connection cache timeout
O ConnectionCacheTimeout=5m

# persistent host status directory
#O HostStatusDirectory=.hoststat

# single thread deliveries (requires HostStatusDirectory)?
#O SingleThreadDelivery=False

# use Errors-To: header?
O UseErrorsTo=False

# log level
O LogLevel=9

# send to me too, even in an alias expansion?
#O MeToo=True

# verify RHS in newaliases?
O CheckAliases=False

# default messages to old style headers if no special punctuation?
O OldStyleHeaders=True

# SMTP daemon options

O DaemonPortOptions=Port=smtp,Addr=0.0.0.0, Name=MTA

# SMTP client options
#O ClientPortOptions=Family=inet, Address=0.0.0.0

# Modifiers to define {daemon_flags} for direct submissions
#O DirectSubmissionModifiers

# Use as mail submission program? See sendmail/SECURITY
#O UseMSP

# privacy flags
O PrivacyOptions=authwarnings,novrfy,noexpn,restrictqrun

# who (if anyone) should get extra copies of error messages
#O PostmasterCopy=Postmaster

# slope of queue-only function
#O QueueFactor=600000

# limit on number of concurrent queue runners
#O MaxQueueChildren

# maximum number of queue-runners per queue-grouping with multiple queues
#O MaxRunnersPerQueue=1

# priority of queue runners (nice(3))
#O NiceQueueRun

# shall we sort the queue by hostname first?
#O QueueSortOrder=priority

# minimum time in queue before retry
#O MinQueueAge=30m

# how many jobs can you process in the queue?
#O MaxQueueRunSize=0

# perform initial split of envelope without checking MX records
#O FastSplit=1

# queue directory
O QueueDirectory=/var/spool/mqueue

# key for shared memory; 0 to turn off, -1 to auto-select
#O SharedMemoryKey=0

# file to store auto-selected key for shared memory (SharedMemoryKey = -1)
#O SharedMemoryKeyFile

# timeouts (many of these)
#O Timeout.initial=5m
O Timeout.connect=1m
#O Timeout.aconnect=0s
#O Timeout.iconnect=5m
#O Timeout.helo=5m
#O Timeout.mail=10m
#O Timeout.rcpt=1h
#O Timeout.datainit=5m
#O Timeout.datablock=1h
#O Timeout.datafinal=1h
#O Timeout.rset=5m
#O Timeout.quit=2m
#O Timeout.misc=2m
#O Timeout.command=1h
O Timeout.ident=0
#O Timeout.fileopen=60s
#O Timeout.control=2m
O Timeout.queuereturn=5d
#O Timeout.queuereturn.normal=5d
#O Timeout.queuereturn.urgent=2d
#O Timeout.queuereturn.non-urgent=7d
#O Timeout.queuereturn.dsn=5d
O Timeout.queuewarn=4h
#O Timeout.queuewarn.normal=4h
#O Timeout.queuewarn.urgent=1h
#O Timeout.queuewarn.non-urgent=12h
#O Timeout.queuewarn.dsn=4h
#O Timeout.hoststatus=30m
#O Timeout.resolver.retrans=5s
#O Timeout.resolver.retrans.first=5s
#O Timeout.resolver.retrans.normal=5s
#O Timeout.resolver.retry=4
#O Timeout.resolver.retry.first=4
#O Timeout.resolver.retry.normal=4
#O Timeout.lhlo=2m
#O Timeout.auth=10m
#O Timeout.starttls=1h

# time for DeliverBy; extension disabled if less than 0
#O DeliverByMin=0

# should we not prune routes in route-addr syntax addresses?
#O DontPruneRoutes=False

# queue up everything before forking?
O SuperSafe=True

# status file
O StatusFile=/var/log/mail/statistics

# time zone handling:
#  if undefined, use system default
#  if defined but null, use TZ envariable passed in
#  if defined and non-null, use that info
#O TimeZoneSpec=

# default UID (can be username or userid:groupid)
O DefaultUser=8:12

# list of locations of user database file (null means no lookup)
O UserDatabaseSpec=/etc/mail/userdb.db

# fallback MX host
#O FallbackMXhost=fall.back.host.net

# fallback smart host
#O FallbackSmartHost=fall.back.host.net

# if we are the best MX host for a site, try it directly instead of config err
O TryNullMXList=True

# load average at which we just queue messages
#O QueueLA=8

# load average at which we refuse connections
#O RefuseLA=12

# log interval when refusing connections for this long
#O RejectLogInterval=3h

# load average at which we delay connections; 0 means no limit
#O DelayLA=0

# maximum number of children we allow at one time
#O MaxDaemonChildren=0

# maximum number of new connections per second
#O ConnectionRateThrottle=0

# Width of the window 
#O ConnectionRateWindowSize=60s

# work recipient factor
#O RecipientFactor=30000

# deliver each queued job in a separate process?
#O ForkEachJob=False

# work class factor
#O ClassFactor=1800

# work time factor
#O RetryFactor=90000

# default character set
#O DefaultCharSet=unknown-8bit

# service switch file (name hardwired on Solaris, Ultrix, OSF/1, others)
#O ServiceSwitchFile=/etc/mail/service.switch

# hosts file (normally /etc/hosts)
#O HostsFile=/etc/hosts

# dialup line delay on connection failure
#O DialDelay=0s

# action to take if there are no recipients in the message
#O NoRecipientAction=none

# chrooted environment for writing to files
#O SafeFileEnvironment

# are colons OK in addresses?
#O ColonOkInAddr=True

# shall I avoid expanding CNAMEs (violates protocols)?
#O DontExpandCnames=False

# SMTP initial login message (old $e macro)
O SmtpGreetingMessage=$j Sendmail $v/$Z; $b

# UNIX initial From header format (old $l macro)
O UnixFromLine=From $g $d

# From: lines that have embedded newlines are unwrapped onto one line
#O SingleLineFromHeader=False

# Allow HELO SMTP command that does not include a host name
#O AllowBogusHELO=False

# Characters to be quoted in a full name phrase (@,;:\()[] are automatic)
#O MustQuoteChars=.

# delimiter (operator) characters (old $o macro)
O OperatorChars=.:%@!^/[]+

# shall I avoid calling initgroups(3) because of high NIS costs?
#O DontInitGroups=False

# are group-writable :include: and .forward files (un)trustworthy?
# True (the default) means they are not trustworthy.
#O UnsafeGroupWrites=True


# where do errors that occur when sending errors get sent?
#O DoubleBounceAddress=postmaster

# issue temporary errors (4xy) instead of permanent errors (5xy)?
#O SoftBounce=False

# where to save bounces if all else fails
#O DeadLetterDrop=/var/tmp/dead.letter

# what user id do we assume for the majority of the processing?
#O RunAsUser=sendmail

# maximum number of recipients per SMTP envelope
#O MaxRecipientsPerMessage=0

# limit the rate recipients per SMTP envelope are accepted
# once the threshold number of recipients have been rejected
#O BadRcptThrottle=0


# shall we get local names from our installed interfaces?
O DontProbeInterfaces=True

# Return-Receipt-To: header implies DSN request
#O RrtImpliesDsn=False

# override connection address (for testing)
#O ConnectOnlyTo=0.0.0.0

# Trusted user for file ownership and starting the daemon
#O TrustedUser=root

# Control socket for daemon management
#O ControlSocketName=/var/spool/mqueue/.control

# Maximum MIME header length to protect MUAs
#O MaxMimeHeaderLength=0/0

# Maximum length of the sum of all headers
#O MaxHeadersLength=32768

# Maximum depth of alias recursion
#O MaxAliasRecursion=10

# location of pid file
#O PidFile=/var/run/sendmail.pid

# Prefix string for the process title shown on 'ps' listings
#O ProcessTitlePrefix=prefix

# Data file (df) memory-buffer file maximum size
#O DataFileBufferSize=4096

# Transcript file (xf) memory-buffer file maximum size
#O XscriptFileBufferSize=4096

# lookup type to find information about local mailboxes
#O MailboxDatabase=pw

# override compile time flag REQUIRES_DIR_FSYNC
#O RequiresDirfsync=true

# list of authentication mechanisms
#O AuthMechanisms=EXTERNAL GSSAPI KERBEROS_V4 DIGEST-MD5 CRAM-MD5

# Authentication realm
#O AuthRealm

# default authentication information for outgoing connections
#O DefaultAuthInfo=/etc/mail/default-auth-info

# SMTP AUTH flags
O AuthOptions=A

# SMTP AUTH maximum encryption strength
#O AuthMaxBits

# SMTP STARTTLS server options
#O TLSSrvOptions


# Input mail filters
#O InputMailFilters


# CA directory
#O CACertPath
# CA file
#O CACertFile
# Server Cert
#O ServerCertFile
# Server private key
#O ServerKeyFile
# Client Cert
#O ClientCertFile
# Client private key
#O ClientKeyFile
# File containing certificate revocation lists 
#O CRLFile
# DHParameters (only required if DSA/DH is used)
#O DHParameters
# Random data source (required for systems without /dev/urandom under OpenSSL)
#O RandFile

# Maximum number of "useless" commands before slowing down
#O MaxNOOPCommands=20

# Name to use for EHLO (defaults to $j)
#O HeloName

############################
# QUEUE GROUP DEFINITIONS  #
############################


###########################
#   Message precedences   #
###########################

Pfirst-class=0
Pspecial-delivery=100
Plist=-30
Pbulk=-60
Pjunk=-100

#####################
#   Trusted users   #
#####################

# this is equivalent to setting class "t"
Ft/etc/mail/trusted-users
Troot
Tdaemon
Tuucp

#########################
#   Format of headers   #
#########################

H?P?Return-Path: <$g>
HReceived: $?sfrom $s $.$?_($?s$|from $.$_)
	$.$?{auth_type}(authenticated$?{auth_ssf} bits=${auth_ssf}$.)
	$.by $j ($v/$Z)$?r with $r$. id $i$?{tls_version}
	(version=${tls_version} cipher=${cipher} bits=${cipher_bits} verify=${verify})$.$?u
	for $u; $|;
	$.$b
H?D?Resent-Date: $a
H?D?Date: $a
H?F?Resent-From: $?x$x <$g>$|$g$.
H?F?From: $?x$x <$g>$|$g$.
H?x?Full-Name: $x
# HPosted-Date: $a
# H?l?Received-Date: $b
H?M?Resent-Message-Id: <$t.$i@$j>
H?M?Message-Id: <$t.$i@$j>

#
######################################################################
######################################################################
#####
#####			REWRITING RULES
#####
######################################################################
######################################################################

############################################
###  Ruleset 3 -- Name Canonicalization  ###
############################################
Scanonify=3

# handle null input (translate to <@> special case)
R$@			$@ <@>

# strip group: syntax (not inside angle brackets!) and trailing semicolon
R$*			$: $1 <@>			mark addresses
R$* < $* > $* <@>	$: $1 < $2 > $3			unmark <addr>
R@ $* <@>		$: @ $1				unmark @host:...
R$* [ IPv6 : $+ ] <@>	$: $1 [ IPv6 : $2 ]		unmark IPv6 addr
R$* :: $* <@>		$: $1 :: $2			unmark node::addr
R:include: $* <@>	$: :include: $1			unmark :include:...
R$* : $* [ $* ]		$: $1 : $2 [ $3 ] <@>		remark if leading colon
R$* : $* <@>		$: $2				strip colon if marked
R$* <@>			$: $1				unmark
R$* ;			   $1				strip trailing semi
R$* < $+ :; > $*	$@ $2 :; <@>			catch <list:;>
R$* < $* ; >		   $1 < $2 >			bogus bracketed semi

# null input now results from list:; syntax
R$@			$@ :; <@>

# strip angle brackets -- note RFC733 heuristic to get innermost item
R$*			$: < $1 >			housekeeping <>
R$+ < $* >		   < $2 >			strip excess on left
R< $* > $+		   < $1 >			strip excess on right
R<>			$@ < @ >			MAIL FROM:<> case
R< $+ >			$: $1				remove housekeeping <>

# strip route address <@a,@b,@c:user@d> -> <user@d>
R@ $+ , $+		$2
R@ [ $* ] : $+		$2
R@ $+ : $+		$2

# find focus for list syntax
R $+ : $* ; @ $+	$@ $>Canonify2 $1 : $2 ; < @ $3 >	list syntax
R $+ : $* ;		$@ $1 : $2;			list syntax

# find focus for @ syntax addresses
R$+ @ $+		$: $1 < @ $2 >			focus on domain
R$+ < $+ @ $+ >		$1 $2 < @ $3 >			move gaze right
R$+ < @ $+ >		$@ $>Canonify2 $1 < @ $2 >	already canonical


# convert old-style addresses to a domain-based address
R$- ! $+		$@ $>Canonify2 $2 < @ $1 .UUCP >	resolve uucp names
R$+ . $- ! $+		$@ $>Canonify2 $3 < @ $1 . $2 >		domain uucps
R$+ ! $+		$@ $>Canonify2 $2 < @ $1 .UUCP >	uucp subdomains

# if we have % signs, take the rightmost one
R$* % $*		$1 @ $2				First make them all @s.
R$* @ $* @ $*		$1 % $2 @ $3			Undo all but the last.
R$* @ $*		$@ $>Canonify2 $1 < @ $2 >	Insert < > and finish

# else we must be a local name
R$*			$@ $>Canonify2 $1


################################################
###  Ruleset 96 -- bottom half of ruleset 3  ###
################################################

SCanonify2=96

# handle special cases for local names
R$* < @ localhost > $*		$: $1 < @ $j . > $2		no domain at all
R$* < @ localhost . $m > $*	$: $1 < @ $j . > $2		local domain
R$* < @ localhost . UUCP > $*	$: $1 < @ $j . > $2		.UUCP domain

# check for IPv4/IPv6 domain literal
R$* < @ [ $+ ] > $*		$: $1 < @@ [ $2 ] > $3		mark [addr]
R$* < @@ $=w > $*		$: $1 < @ $j . > $3		self-literal
R$* < @@ $+ > $*		$@ $1 < @ $2 > $3		canon IP addr





# if really UUCP, handle it immediately

# try UUCP traffic as a local address
R$* < @ $+ . UUCP > $*		$: $1 < @ $[ $2 $] . UUCP . > $3
R$* < @ $+ . . UUCP . > $*	$@ $1 < @ $2 . > $3

# hostnames ending in class P are always canonical
R$* < @ $* $=P > $*		$: $1 < @ $2 $3 . > $4
R$* < @ $* $~P > $*		$: $&{daemon_flags} $| $1 < @ $2 $3 > $4
R$* CC $* $| $* < @ $+.$+ > $*	$: $3 < @ $4.$5 . > $6
R$* CC $* $| $*			$: $3
# pass to name server to make hostname canonical
R$* $| $* < @ $* > $*		$: $2 < @ $[ $3 $] > $4
R$* $| $*			$: $2

# local host aliases and pseudo-domains are always canonical
R$* < @ $=w > $*		$: $1 < @ $2 . > $3
R$* < @ $=M > $*		$: $1 < @ $2 . > $3
R$* < @ $={VirtHost} > $* 	$: $1 < @ $2 . > $3
R$* < @ $* . . > $*		$1 < @ $2 . > $3


##################################################
###  Ruleset 4 -- Final Output Post-rewriting  ###
##################################################
Sfinal=4

R$+ :; <@>		$@ $1 :				handle <list:;>
R$* <@>			$@				handle <> and list:;

# strip trailing dot off possibly canonical name
R$* < @ $+ . > $*	$1 < @ $2 > $3

# eliminate internal code
R$* < @ *LOCAL* > $*	$1 < @ $j > $2

# externalize local domain info
R$* < $+ > $*		$1 $2 $3			defocus
R@ $+ : @ $+ : $+	@ $1 , @ $2 : $3		<route-addr> canonical
R@ $*			$@ @ $1				... and exit

# UUCP must always be presented in old form
R$+ @ $- . UUCP		$2!$1				u@h.UUCP => h!u

# delete duplicate local names
R$+ % $=w @ $=w		$1 @ $2				u%host@host => u@host



##############################################################
###   Ruleset 97 -- recanonicalize and call ruleset zero   ###
###		   (used for recursive calls)		   ###
##############################################################

SRecurse=97
R$*			$: $>canonify $1
R$*			$@ $>parse $1


######################################
###   Ruleset 0 -- Parse Address   ###
######################################

Sparse=0

R$*			$: $>Parse0 $1		initial parsing
R<@>			$#local $: <@>		special case error msgs
R$*			$: $>ParseLocal $1	handle local hacks
R$*			$: $>Parse1 $1		final parsing

#
#  Parse0 -- do initial syntax checking and eliminate local addresses.
#	This should either return with the (possibly modified) input
#	or return with a #error mailer.  It should not return with a
#	#mailer other than the #error mailer.
#

SParse0
R<@>			$@ <@>			special case error msgs
R$* : $* ; <@>		$#error $@ 5.1.3 $: "553 List:; syntax illegal for recipient addresses"
R@ <@ $* >		< @ $1 >		catch "@@host" bogosity
R<@ $+>			$#error $@ 5.1.3 $: "553 User address required"
R$+ <@>			$#error $@ 5.1.3 $: "553 Hostname required"
R$*			$: <> $1
R<> $* < @ [ $* ] : $+ > $*	$1 < @ [ $2 ] : $3 > $4
R<> $* < @ [ $* ] , $+ > $*	$1 < @ [ $2 ] , $3 > $4
R<> $* < @ [ $* ] $+ > $*	$#error $@ 5.1.2 $: "553 Invalid address"
R<> $* < @ [ $+ ] > $*		$1 < @ [ $2 ] > $3
R<> $* <$* : $* > $*	$#error $@ 5.1.3 $: "553 Colon illegal in host name part"
R<> $*			$1
R$* < @ . $* > $*	$#error $@ 5.1.2 $: "553 Invalid host name"
R$* < @ $* .. $* > $*	$#error $@ 5.1.2 $: "553 Invalid host name"
R$* < @ $* @ > $*	$#error $@ 5.1.2 $: "553 Invalid route address"
R$* @ $* < @ $* > $*	$#error $@ 5.1.3 $: "553 Invalid route address"
R$* , $~O $*		$#error $@ 5.1.3 $: "553 Invalid route address"


# now delete the local info -- note $=O to find characters that cause forwarding
R$* < @ > $*		$@ $>Parse0 $>canonify $1	user@ => user
R< @ $=w . > : $*	$@ $>Parse0 $>canonify $2	@here:... -> ...
R$- < @ $=w . >		$: $(dequote $1 $) < @ $2 . >	dequote "foo"@here
R< @ $+ >		$#error $@ 5.1.3 $: "553 User address required"
R$* $=O $* < @ $=w . >	$@ $>Parse0 $>canonify $1 $2 $3	...@here -> ...
R$- 			$: $(dequote $1 $) < @ *LOCAL* >	dequote "foo"
R< @ *LOCAL* >		$#error $@ 5.1.3 $: "553 User address required"
R$* $=O $* < @ *LOCAL* >
			$@ $>Parse0 $>canonify $1 $2 $3	...@*LOCAL* -> ...
R$* < @ *LOCAL* >	$: $1

#
#  Parse1 -- the bottom half of ruleset 0.
#

SParse1

# handle numeric address spec
R$* < @ [ $+ ] > $*	$: $>ParseLocal $1 < @ [ $2 ] > $3	numeric internet spec
R$* < @ [ $+ ] > $*	$: $1 < @ [ $2 ] : $S > $3	Add smart host to path
R$* < @ [ $+ ] : > $*		$#esmtp $@ [$2] $: $1 < @ [$2] > $3	no smarthost: send
R$* < @ [ $+ ] : $- : $*> $*	$#$3 $@ $4 $: $1 < @ [$2] > $5	smarthost with mailer
R$* < @ [ $+ ] : $+ > $*	$#esmtp $@ $3 $: $1 < @ [$2] > $4	smarthost without mailer

# handle virtual users
R$+			$: <!> $1		Mark for lookup
R<!> $+ < @ $={VirtHost} . > 	$: < $(virtuser $1 @ $2 $@ $1 $: @ $) > $1 < @ $2 . >
R<!> $+ < @ $=w . > 	$: < $(virtuser $1 @ $2 $@ $1 $: @ $) > $1 < @ $2 . >
R<@> $+ + $+ < @ $* . >
			$: < $(virtuser $1 + + @ $3 $@ $1 $@ $2 $@ +$2 $: @ $) > $1 + $2 < @ $3 . >
R<@> $+ + $* < @ $* . >
			$: < $(virtuser $1 + * @ $3 $@ $1 $@ $2 $@ +$2 $: @ $) > $1 + $2 < @ $3 . >
R<@> $+ + $* < @ $* . >
			$: < $(virtuser $1 @ $3 $@ $1 $@ $2 $@ +$2 $: @ $) > $1 + $2 < @ $3 . >
R<@> $+ + $+ < @ $+ . >	$: < $(virtuser + + @ $3 $@ $1 $@ $2 $@ +$2 $: @ $) > $1 + $2 < @ $3 . >
R<@> $+ + $* < @ $+ . >	$: < $(virtuser + * @ $3 $@ $1 $@ $2 $@ +$2 $: @ $) > $1 + $2 < @ $3 . >
R<@> $+ + $* < @ $+ . >	$: < $(virtuser @ $3 $@ $1 $@ $2 $@ +$2 $: ! $) > $1 + $2 < @ $3 . >
R<@> $+ < @ $+ . >	$: < $(virtuser @ $2 $@ $1 $: @ $) > $1 < @ $2 . >
R<@> $+			$: $1
R<!> $+			$: $1
R< error : $-.$-.$- : $+ > $* 	$#error $@ $1.$2.$3 $: $4
R< error : $- $+ > $* 	$#error $@ $(dequote $1 $) $: $2
R< $+ > $+ < @ $+ >	$: $>Recurse $1

# short circuit local delivery so forwarded email works


R$=L < @ $=w . >	$#local $: @ $1			special local names
R$+ < @ $=w . >		$#local $: $1			regular local name

# not local -- try mailer table lookup
R$* <@ $+ > $*		$: < $2 > $1 < @ $2 > $3	extract host name
R< $+ . > $*		$: < $1 > $2			strip trailing dot
R< $+ > $*		$: < $(mailertable $1 $) > $2	lookup
R< $~[ : $* > $* 	$>MailerToTriple < $1 : $2 > $3		check -- resolved?
R< $+ > $*		$: $>Mailertable <$1> $2		try domain

# resolve remotely connected UUCP links (if any)

# resolve fake top level domains by forwarding to other hosts



# pass names that still have a host to a smarthost (if defined)
R$* < @ $* > $*		$: $>MailerToTriple < $S > $1 < @ $2 > $3	glue on smarthost name

# deal with other remote names
R$* < @$* > $*		$#esmtp $@ $2 $: $1 < @ $2 > $3	user@host.domain

# handle locally delivered names
R$=L			$#local $: @ $1		special local names
R$+			$#local $: $1			regular local names

###########################################################################
###   Ruleset 5 -- special rewriting after aliases have been expanded   ###
###########################################################################

SLocal_localaddr
Slocaladdr=5
R$+			$: $1 $| $>"Local_localaddr" $1
R$+ $| $#ok		$@ $1			no change
R$+ $| $#$*		$#$2
R$+ $| $*		$: $1




# deal with plussed users so aliases work nicely
R$+ + *			$#local $@ $&h $: $1
R$+ + $*		$#local $@ + $2 $: $1 + *

# prepend an empty "forward host" on the front
R$+			$: <> $1



R< > $+			$: < > < $1 <> $&h >		nope, restore +detail

R< > < $+ <> + $* >	$: < > < $1 + $2 >		check whether +detail
R< > < $+ <> $* >	$: < > < $1 >			else discard
R< > < $+ + $* > $*	   < > < $1 > + $2 $3		find the user part
R< > < $+ > + $*	$#local $@ $2 $: @ $1		strip the extra +
R< > < $+ >		$@ $1				no +detail
R$+			$: $1 <> $&h			add +detail back in

R$+ <> + $*		$: $1 + $2			check whether +detail
R$+ <> $*		$: $1				else discard
R< local : $* > $*	$: $>MailerToTriple < local : $1 > $2	no host extension
R< error : $* > $*	$: $>MailerToTriple < error : $1 > $2	no host extension

R< $~[ : $+ > $+	$: $>MailerToTriple < $1 : $2 > $3 < @ $2 >

R< $+ > $+		$@ $>MailerToTriple < $1 > $2 < @ $1 >


###################################################################
###  Ruleset 90 -- try domain part of mailertable entry 	###
###################################################################

SMailertable=90
R$* <$- . $+ > $*	$: $1$2 < $(mailertable .$3 $@ $1$2 $@ $2 $) > $4
R$* <$~[ : $* > $*	$>MailerToTriple < $2 : $3 > $4		check -- resolved?
R$* < . $+ > $* 	$@ $>Mailertable $1 . <$2> $3		no -- strip & try again
R$* < $* > $*		$: < $(mailertable . $@ $1$2 $) > $3	try "."
R< $~[ : $* > $*	$>MailerToTriple < $1 : $2 > $3		"." found?
R< $* > $*		$@ $2				no mailertable match

###################################################################
###  Ruleset 95 -- canonify mailer:[user@]host syntax to triple	###
###################################################################

SMailerToTriple=95
R< > $*				$@ $1			strip off null relay
R< error : $-.$-.$- : $+ > $* 	$#error $@ $1.$2.$3 $: $4
R< error : $- : $+ > $*		$#error $@ $(dequote $1 $) $: $2
R< error : $+ > $*		$#error $: $1
R< local : $* > $*		$>CanonLocal < $1 > $2
R< $~[ : $+ @ $+ > $*<$*>$*	$# $1 $@ $3 $: $2<@$3>	use literal user
R< $~[ : $+ > $*		$# $1 $@ $2 $: $3	try qualified mailer
R< $=w > $*			$@ $2			delete local host
R< $+ > $*			$#relay $@ $1 $: $2	use unqualified mailer

###################################################################
###  Ruleset CanonLocal -- canonify local: syntax		###
###################################################################

SCanonLocal
# strip local host from routed addresses
R< $* > < @ $+ > : $+		$@ $>Recurse $3
R< $* > $+ $=O $+ < @ $+ >	$@ $>Recurse $2 $3 $4

# strip trailing dot from any host name that may appear
R< $* > $* < @ $* . >		$: < $1 > $2 < @ $3 >

# handle local: syntax -- use old user, either with or without host
R< > $* < @ $* > $*		$#local $@ $1@$2 $: $1
R< > $+				$#local $@ $1    $: $1

# handle local:user@host syntax -- ignore host part
R< $+ @ $+ > $* < @ $* >	$: < $1 > $3 < @ $4 >

# handle local:user syntax
R< $+ > $* <@ $* > $*		$#local $@ $2@$3 $: $1
R< $+ > $* 			$#local $@ $2    $: $1

###################################################################
###  Ruleset 93 -- convert header names to masqueraded form	###
###################################################################

SMasqHdr=93


# do not masquerade anything in class N
R$* < @ $* $=N . >	$@ $1 < @ $2 $3 . >

R$* < @ *LOCAL* >	$@ $1 < @ $j . >

###################################################################
###  Ruleset 94 -- convert envelope names to masqueraded form	###
###################################################################

SMasqEnv=94
R$* < @ *LOCAL* > $*	$: $1 < @ $j . > $2

###################################################################
###  Ruleset 98 -- local part of ruleset zero (can be null)	###
###################################################################

SParseLocal=98

# addresses sent to foo@host.REDIRECT will give a 551 error code
R$* < @ $+ .REDIRECT. >		$: $1 < @ $2 . REDIRECT . > < ${opMode} >
R$* < @ $+ .REDIRECT. > <i>	$: $1 < @ $2 . REDIRECT. >
R$* < @ $+ .REDIRECT. > < $- >	$#error $@ 5.1.1 $: "551 User has moved; please try " <$1@$2>




######################################################################
###  D: LookUpDomain -- search for domain in access database
###
###	Parameters:
###		<$1> -- key (domain name)
###		<$2> -- default (what to return if not found in db)
###		<$3> -- mark (must be <(!|+) single-token>)
###			! does lookup only with tag
###			+ does lookup with and without tag
###		<$4> -- passthru (additional data passed unchanged through)
######################################################################

SD
R<$*> <$+> <$- $-> <$*>		$: < $(access $4:$1 $: ? $) > <$1> <$2> <$3 $4> <$5>
R<?> <$+> <$+> <+ $-> <$*>	$: < $(access $1 $: ? $) > <$1> <$2> <+ $3> <$4>
R<?> <[$+.$-]> <$+> <$- $-> <$*>	$@ $>D <[$1]> <$3> <$4 $5> <$6>
R<?> <[$+::$-]> <$+> <$- $-> <$*>	$: $>D <[$1]> <$3> <$4 $5> <$6>
R<?> <[$+:$-]> <$+> <$- $-> <$*>	$: $>D <[$1]> <$3> <$4 $5> <$6>
R<?> <$+.$+> <$+> <$- $-> <$*>	$@ $>D <$2> <$3> <$4 $5> <$6>
R<?> <$+> <$+> <$- $-> <$*>	$@ <$2> <$5>
R<$* <TMPF>> <$+> <$+> <$- $-> <$*>	$@ <<TMPF>> <$6>
R<$*> <$+> <$+> <$- $-> <$*>	$@ <$1> <$6>

######################################################################
###  A: LookUpAddress -- search for host address in access database
###
###	Parameters:
###		<$1> -- key (dot quadded host address)
###		<$2> -- default (what to return if not found in db)
###		<$3> -- mark (must be <(!|+) single-token>)
###			! does lookup only with tag
###			+ does lookup with and without tag
###		<$4> -- passthru (additional data passed through)
######################################################################

SA
R<$+> <$+> <$- $-> <$*>		$: < $(access $4:$1 $: ? $) > <$1> <$2> <$3 $4> <$5>
R<?> <$+> <$+> <+ $-> <$*>	$: < $(access $1 $: ? $) > <$1> <$2> <+ $3> <$4>
R<?> <$+::$-> <$+> <$- $-> <$*>		$@ $>A <$1> <$3> <$4 $5> <$6>
R<?> <$+:$-> <$+> <$- $-> <$*>		$@ $>A <$1> <$3> <$4 $5> <$6>
R<?> <$+.$-> <$+> <$- $-> <$*>		$@ $>A <$1> <$3> <$4 $5> <$6>
R<?> <$+> <$+> <$- $-> <$*>	$@ <$2> <$5>
R<$* <TMPF>> <$+> <$+> <$- $-> <$*>	$@ <<TMPF>> <$6>
R<$*> <$+> <$+> <$- $-> <$*>	$@ <$1> <$6>

######################################################################
###  CanonAddr --	Convert an address into a standard form for
###			relay checking.  Route address syntax is
###			crudely converted into a %-hack address.
###
###	Parameters:
###		$1 -- full recipient address
###
###	Returns:
###		parsed address, not in source route form
######################################################################

SCanonAddr
R$*			$: $>Parse0 $>canonify $1	make domain canonical


######################################################################
###  ParseRecipient --	Strip off hosts in $=R as well as possibly
###			$* $=m or the access database.
###			Check user portion for host separators.
###
###	Parameters:
###		$1 -- full recipient address
###
###	Returns:
###		parsed, non-local-relaying address
######################################################################

SParseRecipient
R$*				$: <?> $>CanonAddr $1
R<?> $* < @ $* . >		<?> $1 < @ $2 >			strip trailing dots
R<?> $- < @ $* >		$: <?> $(dequote $1 $) < @ $2 >	dequote local part

# if no $=O character, no host in the user portion, we are done
R<?> $* $=O $* < @ $* >		$: <NO> $1 $2 $3 < @ $4>
R<?> $*				$@ $1


R<NO> $* < @ $* $=R >		$: <RELAY> $1 < @ $2 $3 >
R<NO> $* < @ $+ >		$: $>D <$2> <NO> <+ To> <$1 < @ $2 >>
R<$+> <$+>			$: <$1> $2



R<RELAY> $* < @ $* >		$@ $>ParseRecipient $1
R<$+> $*			$@ $2


######################################################################
###  check_relay -- check hostname/address on SMTP startup
######################################################################



SLocal_check_relay
Scheck_relay
R$*			$: $1 $| $>"Local_check_relay" $1
R$* $| $* $| $#$*	$#$3
R$* $| $* $| $*		$@ $>"Basic_check_relay" $1 $| $2

SBasic_check_relay
# check for deferred delivery mode
R$*			$: < $&{deliveryMode} > $1
R< d > $*		$@ deferred
R< $* > $*		$: $2

R$+ $| $+		$: $>D < $1 > <?> <+ Connect> < $2 >
R   $| $+		$: $>A < $1 > <?> <+ Connect> <>	empty client_name
R<?> <$+>		$: $>A < $1 > <?> <+ Connect> <>	no: another lookup
R<?> <$*>		$: OK				found nothing
R<$={Accept}> <$*>	$@ $1				return value of lookup
R<REJECT> <$*>		$#error $@ 5.7.1 $: "550 Access denied"
R<DISCARD> <$*>		$#discard $: discard
R<QUARANTINE:$+> <$*>	$#error $@ quarantine $: $1
R<ERROR:$-.$-.$-:$+> <$*>	$#error $@ $1.$2.$3 $: $4
R<ERROR:$+> <$*>		$#error $: $1
R<$* <TMPF>> <$*>		$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<$+> <$*>		$#error $: $1



######################################################################
###  check_mail -- check SMTP `MAIL FROM:' command argument
######################################################################

SLocal_check_mail
Scheck_mail
R$*			$: $1 $| $>"Local_check_mail" $1
R$* $| $#$*		$#$2
R$* $| $*		$@ $>"Basic_check_mail" $1

SBasic_check_mail
# check for deferred delivery mode
R$*			$: < $&{deliveryMode} > $1
R< d > $*		$@ deferred
R< $* > $*		$: $2

# authenticated?
R$*			$: $1 $| $>"tls_client" $&{verify} $| MAIL
R$* $| $#$+		$#$2
R$* $| $*		$: $1

R<>			$@ <OK>			we MUST accept <> (RFC 1123)
R$+			$: <?> $1
R<?><$+>		$: <@> <$1>
R<?>$+			$: <@> <$1>
R$*			$: $&{daemon_flags} $| $1
R$* f $* $| <@> < $* @ $- >	$: < ? $&{client_name} > < $3 @ $4 >
R$* u $* $| <@> < $* >	$: <?> < $3 >
R$* $| $*		$: $2
# handle case of @localhost on address
R<@> < $* @ localhost >	$: < ? $&{client_name} > < $1 @ localhost >
R<@> < $* @ [127.0.0.1] >
			$: < ? $&{client_name} > < $1 @ [127.0.0.1] >
R<@> < $* @ localhost.$m >
			$: < ? $&{client_name} > < $1 @ localhost.$m >
R<@> < $* @ localhost.localdomain >
			$: < ? $&{client_name} > < $1 @ localhost.localdomain >
R<@> < $* @ localhost.UUCP >
			$: < ? $&{client_name} > < $1 @ localhost.UUCP >
R<@> $*			$: $1			no localhost as domain
R<? $=w> $*		$: $2			local client: ok
R<? $+> <$+>		$#error $@ 5.5.4 $: "553 Real domain name required for sender address"
R<?> $*			$: $1
R$*			$: <?> $>CanonAddr $1		canonify sender address and mark it
R<?> $* < @ $+ . >	<?> $1 < @ $2 >			strip trailing dots
# handle non-DNS hostnames (*.bitnet, *.decnet, *.uucp, etc)
R<?> $* < @ $* $=P >	$: <OKR> $1 < @ $2 $3 >
R<?> $* < @ $j >	$: <OKR> $1 < @ $j >
R<?> $* < @ $+ >	$: <OKR> $1 < @ $2 >		... unresolvable OK

# check sender address: user@address, user@, address
R<$+> $+ < @ $* >	$: @<$1> <$2 < @ $3 >> $| <F:$2@$3> <U:$2@> <D:$3>
R<$+> $+		$: @<$1> <$2> $| <U:$2@>
R@ <$+> <$*> $| <$+>	$: <@> <$1> <$2> $| $>SearchList <+ From> $| <$3> <>
R<@> <$+> <$*> $| <$*>	$: <$3> <$1> <$2>		reverse result
# retransform for further use
R<?> <$+> <$*>		$: <$1> $2	no match
R<$+> <$+> <$*>		$: <$1> $3	relevant result, keep it

# handle case of no @domain on address
R<?> $*			$: $&{daemon_flags} $| <?> $1
R$* u $* $| <?> $*	$: <OKR> $3
R$* $| $*		$: $2
R<?> $*			$: < ? $&{client_addr} > $1
R<?> $*			$@ <OKR>			...local unqualed ok
R<? $+> $*		$#error $@ 5.5.4 $: "553 Domain name required for sender address " $&f
							...remote is not
# check results
R<?> $*			$: @ $1		mark address: nothing known about it
R<$={ResOk}> $*		$: @ $2		domain ok
R<TEMP> $*		$#error $@ 4.1.8 $: "451 Domain of sender address " $&f " does not resolve"
R<PERM> $*		$#error $@ 5.1.8 $: "553 Domain of sender address " $&f " does not exist"
R<$={Accept}> $*	$# $1		accept from access map
R<DISCARD> $*		$#discard $: discard
R<QUARANTINE:$+> $*	$#error $@ quarantine $: $1
R<REJECT> $*		$#error $@ 5.7.1 $: "550 Access denied"
R<ERROR:$-.$-.$-:$+> $*		$#error $@ $1.$2.$3 $: $4
R<ERROR:$+> $*		$#error $: $1
R<<TMPF>> $*		$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<$+> $*		$#error $: $1		error from access db



######################################################################
###  check_rcpt -- check SMTP `RCPT TO:' command argument
######################################################################

SLocal_check_rcpt
Scheck_rcpt
R$*			$: $1 $| $>"Local_check_rcpt" $1
R$* $| $#$*		$#$2
R$* $| $*		$@ $>"Basic_check_rcpt" $1

SBasic_check_rcpt
# empty address?
R<>			$#error $@ nouser $: "553 User address required"
R$@			$#error $@ nouser $: "553 User address required"
# check for deferred delivery mode
R$*			$: < $&{deliveryMode} > $1
R< d > $*		$@ deferred
R< $* > $*		$: $2


######################################################################
R$*			$: $1 $| @ $>"Rcpt_ok" $1
R$* $| @ $#TEMP $+	$: $1 $| T $2
R$* $| @ $#$*		$#$2
R$* $| @ RELAY		$@ RELAY
R$* $| @ $*		$: O $| $>"Relay_ok" $1
R$* $| T $+		$: T $2 $| $>"Relay_ok" $1
R$* $| $#TEMP $+	$#error $2
R$* $| $#$*		$#$2
R$* $| RELAY		$@ RELAY
R T $+ $| $*		$#error $1
# anything else is bogus
R$*			$#error $@ 5.7.1 $: "550 Relaying denied"


######################################################################
### Rcpt_ok: is the recipient ok?
######################################################################
SRcpt_ok
R$*			$: $>ParseRecipient $1		strip relayable hosts



# blacklist local users or any host from receiving mail
R$*			$: <?> $1
R<?> $+ < @ $=w >	$: <> <$1 < @ $2 >> $| <F:$1@$2> <U:$1@> <D:$2>
R<?> $+ < @ $* >	$: <> <$1 < @ $2 >> $| <F:$1@$2> <D:$2>
R<?> $+			$: <> <$1> $| <U:$1@>
R<> <$*> $| <$+>	$: <@> <$1> $| $>SearchList <+ To> $| <$2> <>
R<@> <$*> $| <$*>	$: <$2> <$1>		reverse result
R<?> <$*>		$: @ $1		mark address as no match
R<$={Accept}> <$*>	$: @ $2		mark address as no match

R<REJECT> $*		$#error $@ 5.2.1 $: "550 Mailbox disabled for this recipient"
R<DISCARD> $*		$#discard $: discard
R<QUARANTINE:$+> $*	$#error $@ quarantine $: $1
R<ERROR:$-.$-.$-:$+> $*		$#error $@ $1.$2.$3 $: $4
R<ERROR:$+> $*		$#error $: $1
R<<TMPF>> $*		$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<$+> $*		$#error $: $1		error from access db
R@ $*			$1		remove mark

# authenticated via TLS?
R$*			$: $1 $| $>RelayTLS	client authenticated?
R$* $| $# $+		$# $2			error/ok?
R$* $| $*		$: $1			no

R$*			$: $1 $| $>"Local_Relay_Auth" $&{auth_type}
R$* $| $# $*		$# $2
R$* $| NO		$: $1
R$* $| $*		$: $1 $| $&{auth_type}
R$* $|			$: $1
R$* $| $={TrustAuthMech}	$# RELAY
R$* $| $*		$: $1
# anything terminating locally is ok
R$+ < @ $=w >		$@ RELAY
R$+ < @ $* $=R >	$@ RELAY
R$+ < @ $+ >		$: $>D <$2> <?> <+ To> <$1 < @ $2 >>
R<RELAY> $*		$@ RELAY
R<$* <TMPF>> $*		$#TEMP $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<$*> <$*>		$: $2



# check for local user (i.e. unqualified address)
R$*			$: <?> $1
R<?> $* < @ $+ >	$: <REMOTE> $1 < @ $2 >
# local user is ok
R<?> $+			$@ RELAY
R<$+> $*		$: $2

######################################################################
### Relay_ok: is the relay/sender ok?
######################################################################
SRelay_ok
# anything originating locally is ok
# check IP address
R$*			$: $&{client_addr}
R$@			$@ RELAY		originated locally
R0			$@ RELAY		originated locally
R127.0.0.1		$@ RELAY		originated locally
RIPv6:::1		$@ RELAY		originated locally
R$=R $*			$@ RELAY		relayable IP address
R$*			$: $>A <$1> <?> <+ Connect> <$1>
R<RELAY> $* 		$@ RELAY		relayable IP address

R<<TMPF>> $*		$#TEMP $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<$*> <$*>		$: $2
R$*			$: [ $1 ]		put brackets around it...
R$=w			$@ RELAY		... and see if it is local


# check client name: first: did it resolve?
R$*			$: < $&{client_resolve} >
R<TEMP>			$#TEMP $@ 4.4.0 $: "450 Relaying temporarily denied. Cannot resolve PTR record for " $&{client_addr}
R<FORGED>		$#error $@ 5.7.1 $: "550 Relaying denied. IP name possibly forged " $&{client_name}
R<FAIL>			$#error $@ 5.7.1 $: "550 Relaying denied. IP name lookup failed " $&{client_name}
R$*			$: <@> $&{client_name}
# pass to name server to make hostname canonical
R<@> $* $=P 		$:<?>  $1 $2
R<@> $+			$:<?>  $[ $1 $]
R$* .			$1			strip trailing dots
R<?> $=w		$@ RELAY
R<?> $* $=R			$@ RELAY
R<?> $*			$: $>D <$1> <?> <+ Connect> <$1>
R<RELAY> $*		$@ RELAY
R<$* <TMPF>> $*		$#TEMP $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<$*> <$*>		$: $2



######################################################################
###  F: LookUpFull -- search for an entry in access database
###
###	lookup of full key (which should be an address) and
###	variations if +detail exists: +* and without +detail
###
###	Parameters:
###		<$1> -- key
###		<$2> -- default (what to return if not found in db)
###		<$3> -- mark (must be <(!|+) single-token>)
###			! does lookup only with tag
###			+ does lookup with and without tag
###		<$4> -- passthru (additional data passed unchanged through)
######################################################################

SF
R<$+> <$*> <$- $-> <$*>		$: <$(access $4:$1 $: ? $)> <$1> <$2> <$3 $4> <$5>
R<?> <$+> <$*> <+ $-> <$*>	$: <$(access $1 $: ? $)> <$1> <$2> <+ $3> <$4>
R<?> <$+ + $* @ $+> <$*> <$- $-> <$*>
			$: <$(access $6:$1+*@$3 $: ? $)> <$1+$2@$3> <$4> <$5 $6> <$7>
R<?> <$+ + $* @ $+> <$*> <+ $-> <$*>
			$: <$(access $1+*@$3 $: ? $)> <$1+$2@$3> <$4> <+ $5> <$6>
R<?> <$+ + $* @ $+> <$*> <$- $-> <$*>
			$: <$(access $6:$1@$3 $: ? $)> <$1+$2@$3> <$4> <$5 $6> <$7>
R<?> <$+ + $* @ $+> <$*> <+ $-> <$*>
			$: <$(access $1@$3 $: ? $)> <$1+$2@$3> <$4> <+ $5> <$6>
R<?> <$+> <$*> <$- $-> <$*>	$@ <$2> <$5>
R<$+ <TMPF>> <$*> <$- $-> <$*>	$@ <<TMPF>> <$5>
R<$+> <$*> <$- $-> <$*>		$@ <$1> <$5>

######################################################################
###  E: LookUpExact -- search for an entry in access database
###
###	Parameters:
###		<$1> -- key
###		<$2> -- default (what to return if not found in db)
###		<$3> -- mark (must be <(!|+) single-token>)
###			! does lookup only with tag
###			+ does lookup with and without tag
###		<$4> -- passthru (additional data passed unchanged through)
######################################################################

SE
R<$*> <$*> <$- $-> <$*>		$: <$(access $4:$1 $: ? $)> <$1> <$2> <$3 $4> <$5>
R<?> <$+> <$*> <+ $-> <$*>	$: <$(access $1 $: ? $)> <$1> <$2> <+ $3> <$4>
R<?> <$+> <$*> <$- $-> <$*>	$@ <$2> <$5>
R<$+ <TMPF>> <$*> <$- $-> <$*>	$@ <<TMPF>> <$5>
R<$+> <$*> <$- $-> <$*>		$@ <$1> <$5>

######################################################################
###  U: LookUpUser -- search for an entry in access database
###
###	lookup of key (which should be a local part) and
###	variations if +detail exists: +* and without +detail
###
###	Parameters:
###		<$1> -- key (user@)
###		<$2> -- default (what to return if not found in db)
###		<$3> -- mark (must be <(!|+) single-token>)
###			! does lookup only with tag
###			+ does lookup with and without tag
###		<$4> -- passthru (additional data passed unchanged through)
######################################################################

SU
R<$+> <$*> <$- $-> <$*>		$: <$(access $4:$1 $: ? $)> <$1> <$2> <$3 $4> <$5>
R<?> <$+> <$*> <+ $-> <$*>	$: <$(access $1 $: ? $)> <$1> <$2> <+ $3> <$4>
R<?> <$+ + $* @> <$*> <$- $-> <$*>
			$: <$(access $5:$1+*@ $: ? $)> <$1+$2@> <$3> <$4 $5> <$6>
R<?> <$+ + $* @> <$*> <+ $-> <$*>
			$: <$(access $1+*@ $: ? $)> <$1+$2@> <$3> <+ $4> <$5>
R<?> <$+ + $* @> <$*> <$- $-> <$*>
			$: <$(access $5:$1@ $: ? $)> <$1+$2@> <$3> <$4 $5> <$6>
R<?> <$+ + $* @> <$*> <+ $-> <$*>
			$: <$(access $1@ $: ? $)> <$1+$2@> <$3> <+ $4> <$5>
R<?> <$+> <$*> <$- $-> <$*>	$@ <$2> <$5>
R<$+ <TMPF>> <$*> <$- $-> <$*>	$@ <<TMPF>> <$5>
R<$+> <$*> <$- $-> <$*>		$@ <$1> <$5>

######################################################################
###  SearchList: search a list of items in the access map
###	Parameters:
###		<exact tag> $| <mark:address> <mark:address> ... <>
###	where "exact" is either "+" or "!":
###	<+ TAG>	lookup with and w/o tag
###	<! TAG>	lookup with tag
###	possible values for "mark" are:
###		D: recursive host lookup (LookUpDomain)
###		E: exact lookup, no modifications
###		F: full lookup, try user+ext@domain and user@domain
###		U: user lookup, try user+ext and user (input must have trailing @)
###	return: <RHS of lookup> or <?> (not found)
######################################################################

# class with valid marks for SearchList
C{Src}E F D U 
SSearchList
# just call the ruleset with the name of the tag... nice trick...
R<$+> $| <$={Src}:$*> <$*>	$: <$1> $| <$4> $| $>$2 <$3> <?> <$1> <>
R<$+> $| <> $| <?> <>		$@ <?>
R<$+> $| <$+> $| <?> <>		$@ $>SearchList <$1> $| <$2>
R<$+> $| <$*> $| <$+> <>	$@ <$3>
R<$+> $| <$+>			$@ <$2>


######################################################################
###  trust_auth: is user trusted to authenticate as someone else?
###
###	Parameters:
###		$1: AUTH= parameter from MAIL command
######################################################################

SLocal_trust_auth
Strust_auth
R$*			$: $&{auth_type} $| $1
# required by RFC 2554 section 4.
R$@ $| $*		$#error $@ 5.7.1 $: "550 not authenticated"
R$* $| $&{auth_authen}		$@ identical
R$* $| <$&{auth_authen}>	$@ identical
R$* $| $*		$: $1 $| $>"Local_trust_auth" $2
R$* $| $#$*		$#$2
R$*			$#error $@ 5.7.1 $: "550 " $&{auth_authen} " not allowed to act as " $&{auth_author}

######################################################################
###  Relay_Auth: allow relaying based on authentication?
###
###	Parameters:
###		$1: ${auth_type}
######################################################################
SLocal_Relay_Auth

######################################################################
###  srv_features: which features to offer to a client?
###	(done in server)
######################################################################
Ssrv_features
R$*		$: $>D <$&{client_name}> <?> <! "Srv_Features"> <>
R<?>$*		$: $>A <$&{client_addr}> <?> <! "Srv_Features"> <>
R<?>$*		$: <$(access "Srv_Features": $: ? $)>
R<?>$*		$@ OK
R<$* <TMPF>>$*	$#temp
R<$+>$*		$# $1

######################################################################
###  try_tls: try to use STARTTLS?
###	(done in client)
######################################################################
Stry_tls
R$*		$: $>D <$&{server_name}> <?> <! "Try_TLS"> <>
R<?>$*		$: $>A <$&{server_addr}> <?> <! "Try_TLS"> <>
R<?>$*		$: <$(access "Try_TLS": $: ? $)>
R<?>$*		$@ OK
R<$* <TMPF>>$*	$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R<NO>$*		$#error $@ 5.7.1 $: "550 do not try TLS with " $&{server_name} " ["$&{server_addr}"]"

######################################################################
###  tls_rcpt: is connection with server "good" enough?
###	(done in client, per recipient)
###
###	Parameters:
###		$1: recipient
######################################################################
Stls_rcpt
R$*			$: $(macro {TLS_Name} $@ $&{server_name} $) $1
R$+			$: <?> $>CanonAddr $1
R<?> $+ < @ $+ . >	<?> $1 <@ $2 >
R<?> $+ < @ $+ >	$: $1 <@ $2 > $| <F:$1@$2> <U:$1@> <D:$2> <E:>
R<?> $+			$: $1 $| <U:$1@> <E:>
R$* $| $+	$: $1 $| $>SearchList <! "TLS_Rcpt"> $| $2 <>
R$* $| <?>	$@ OK
R$* $| <$* <TMPF>>	$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R$* $| <$+>	$@ $>"TLS_connection" $&{verify} $| <$2>

######################################################################
###  tls_client: is connection with client "good" enough?
###	(done in server)
###
###	Parameters:
###		${verify} $| (MAIL|STARTTLS)
######################################################################
Stls_client
R$*		$: $(macro {TLS_Name} $@ $&{client_name} $) $1
R$* $| $*	$: $1 $| $>D <$&{client_name}> <?> <! "TLS_Clt"> <>
R$* $| <?>$*	$: $1 $| $>A <$&{client_addr}> <?> <! "TLS_Clt"> <>
R$* $| <?>$*	$: $1 $| <$(access "TLS_Clt": $: ? $)>
R$* $| <$* <TMPF>>	$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R$*		$@ $>"TLS_connection" $1

######################################################################
###  tls_server: is connection with server "good" enough?
###	(done in client)
###
###	Parameter:
###		${verify}
######################################################################
Stls_server
R$*		$: $(macro {TLS_Name} $@ $&{server_name} $) $1
R$*		$: $1 $| $>D <$&{server_name}> <?> <! "TLS_Srv"> <>
R$* $| <?>$*	$: $1 $| $>A <$&{server_addr}> <?> <! "TLS_Srv"> <>
R$* $| <?>$*	$: $1 $| <$(access "TLS_Srv": $: ? $)>
R$* $| <$* <TMPF>>	$#error $@ 4.3.0 $: "451 Temporary system failure. Please try again later."
R$*		$@ $>"TLS_connection" $1

######################################################################
###  TLS_connection: is TLS connection "good" enough?
###
###	Parameters:
###		${verify} $| <Requirement> [<>]
###		Requirement: RHS from access map, may be ? for none.
######################################################################
STLS_connection
R$* $| <$*>$*			$: $1 $| <$2>
# create the appropriate error codes
R$* $| <PERM + $={Tls} $*>	$: $1 $| <503:5.7.0> <$2 $3>
R$* $| <TEMP + $={Tls} $*>	$: $1 $| <403:4.7.0> <$2 $3>
R$* $| <$={Tls} $*>		$: $1 $| <403:4.7.0> <$2 $3>
# deal with TLS handshake failures: abort
RSOFTWARE $| <$-:$+> $* 	$#error $@ $2 $: $1 " TLS handshake failed."
RSOFTWARE $| $* 		$#error $@ 4.7.0 $: "403 TLS handshake failed."
# deal with TLS protocol errors: abort
RPROTOCOL $| <$-:$+> $* 	$#error $@ $2 $: $1 " STARTTLS failed."
RPROTOCOL $| $* 		$#error $@ 4.7.0 $: "403 STARTTLS failed."
R$* $| <$*> <VERIFY>		$: <$2> <VERIFY> <> $1
R$* $| <$*> <VERIFY + $+>	$: <$2> <VERIFY> <$3> $1
R$* $| <$*> <$={Tls}:$->$*	$: <$2> <$3:$4> <> $1
R$* $| <$*> <$={Tls}:$- + $+>$*	$: <$2> <$3:$4> <$5> $1
R$* $| $*			$@ OK
# authentication required: give appropriate error
# other side did authenticate (via STARTTLS)
R<$*><VERIFY> <> OK		$@ OK
R<$*><VERIFY> <$+> OK		$: <$1> <REQ:0> <$2>
R<$*><VERIFY:$-> <$*> OK	$: <$1> <REQ:$2> <$3>
R<$*><ENCR:$-> <$*> $*		$: <$1> <REQ:$2> <$3>
R<$-:$+><VERIFY $*> <$*>	$#error $@ $2 $: $1 " authentication required"
R<$-:$+><VERIFY $*> <$*> FAIL	$#error $@ $2 $: $1 " authentication failed"
R<$-:$+><VERIFY $*> <$*> NO	$#error $@ $2 $: $1 " not authenticated"
R<$-:$+><VERIFY $*> <$*> NOT	$#error $@ $2 $: $1 " no authentication requested"
R<$-:$+><VERIFY $*> <$*> NONE	$#error $@ $2 $: $1 " other side does not support STARTTLS"
R<$-:$+><VERIFY $*> <$*> $+	$#error $@ $2 $: $1 " authentication failure " $4
R<$*><REQ:$-> <$*>		$: <$1> <REQ:$2> <$3> $>max $&{cipher_bits} : $&{auth_ssf}
R<$*><REQ:$-> <$*> $-		$: <$1> <$2:$4> <$3> $(arith l $@ $4 $@ $2 $)
R<$-:$+><$-:$-> <$*> TRUE	$#error $@ $2 $: $1 " encryption too weak " $4 " less than " $3
R<$-:$+><$-:$-> <$*> $*		$: <$1:$2 ++ $5>
R<$-:$+ ++ >			$@ OK
R<$-:$+ ++ $+ >			$: <$1:$2> <$3>
R<$-:$+> < $+ ++ $+ >		<$1:$2> <$3> <$4>
R<$-:$+> $+			$@ $>"TLS_req" $3 $| <$1:$2>

######################################################################
###  TLS_req: check additional TLS requirements
###
###	Parameters: [<list> <of> <req>] $| <$-:$+>
###		$-: SMTP reply code
###		$+: Enhanced Status Code
######################################################################
STLS_req
R $| $+		$@ OK
R<CN> $* $| <$+>		$: <CN:$&{TLS_Name}> $1 $| <$2>
R<CN:$&{cn_subject}> $* $| <$+>		$@ $>"TLS_req" $1 $| <$2>
R<CN:$+> $* $| <$-:$+>	$#error $@ $4 $: $3 " CN " $&{cn_subject} " does not match " $1
R<CS:$&{cert_subject}> $* $| <$+>	$@ $>"TLS_req" $1 $| <$2>
R<CS:$+> $* $| <$-:$+>	$#error $@ $4 $: $3 " Cert Subject " $&{cert_subject} " does not match " $1
R<CI:$&{cert_issuer}> $* $| <$+>	$@ $>"TLS_req" $1 $| <$2>
R<CI:$+> $* $| <$-:$+>	$#error $@ $4 $: $3 " Cert Issuer " $&{cert_issuer} " does not match " $1
ROK			$@ OK

######################################################################
###  max: return the maximum of two values separated by :
###
###	Parameters: [$-]:[$-]
######################################################################
Smax
R:		$: 0
R:$-		$: $1
R$-:		$: $1
R$-:$-		$: $(arith l $@ $1 $@ $2 $) : $1 : $2
RTRUE:$-:$-	$: $2
R$-:$-:$-	$: $2


######################################################################
###  RelayTLS: allow relaying based on TLS authentication
###
###	Parameters:
###		none
######################################################################
SRelayTLS
# authenticated?
R$*			$: <?> $&{verify}
R<?> OK			$: OK		authenticated: continue
R<?> $*			$@ NO		not authenticated
R$*			$: $&{cert_issuer}
R$+			$: $(access CERTISSUER:$1 $)
RRELAY			$# RELAY
RSUBJECT		$: <@> $&{cert_subject}
R<@> $+			$: <@> $(access CERTSUBJECT:$1 $)
R<@> RELAY		$# RELAY
R$*			$: NO

######################################################################
###  authinfo: lookup authinfo in the access map
###
###	Parameters:
###		$1: {server_name}
###		$2: {server_addr}
######################################################################
Sauthinfo
R$*		$: $1 $| $>D <$&{server_name}> <?> <! AuthInfo> <>
R$* $| <?>$*	$: $1 $| $>A <$&{server_addr}> <?> <! AuthInfo> <>
R$* $| <?>$*	$: $1 $| <$(access AuthInfo: $: ? $)> <>
R$* $| <?>$*	$@ no				no authinfo available
R$* $| <$*> <>	$# $2





#
######################################################################
######################################################################
#####
#####			MAIL FILTER DEFINITIONS
#####
######################################################################
######################################################################

#
######################################################################
######################################################################
#####
#####			MAILER DEFINITIONS
#####
######################################################################
######################################################################

#####################################
###   SMTP Mailer specification   ###
#####################################

#####  $Id: smtp.m4,v 8.65 2006/07/12 21:08:10 ca Exp $  #####

#
#  common sender and masquerading recipient rewriting
#
SMasqSMTP
R$* < @ $* > $*		$@ $1 < @ $2 > $3		already fully qualified
R$+			$@ $1 < @ *LOCAL* >		add local qualification

#
#  convert pseudo-domain addresses to real domain addresses
#
SPseudoToReal

# pass <route-addr>s through
R< @ $+ > $*		$@ < @ $1 > $2			resolve <route-addr>

# output fake domains as user%fake@relay

# do UUCP heuristics; note that these are shared with UUCP mailers
R$+ < @ $+ .UUCP. >	$: < $2 ! > $1			convert to UUCP form
R$+ < @ $* > $*		$@ $1 < @ $2 > $3		not UUCP form

# leave these in .UUCP form to avoid further tampering
R< $&h ! > $- ! $+	$@ $2 < @ $1 .UUCP. >
R< $&h ! > $-.$+ ! $+	$@ $3 < @ $1.$2 >
R< $&h ! > $+		$@ $1 < @ $&h .UUCP. >
R< $+ ! > $+		$: $1 ! $2 < @ $Y >		use UUCP_RELAY
R$+ < @ $~[ $* : $+ >	$@ $1 < @ $4 >			strip mailer: part
R$+ < @ >		$: $1 < @ *LOCAL* >		if no UUCP_RELAY


#
#  envelope sender rewriting
#
SEnvFromSMTP
R$+			$: $>PseudoToReal $1		sender/recipient common
R$* :; <@>		$@				list:; special case
R$*			$: $>MasqSMTP $1		qualify unqual'ed names
R$+			$: $>MasqEnv $1			do masquerading


#
#  envelope recipient rewriting --
#  also header recipient if not masquerading recipients
#
SEnvToSMTP
R$+			$: $>PseudoToReal $1		sender/recipient common
R$+			$: $>MasqSMTP $1		qualify unqual'ed names
R$* < @ *LOCAL* > $*	$: $1 < @ $j . > $2

#
#  header sender and masquerading header recipient rewriting
#
SHdrFromSMTP
R$+			$: $>PseudoToReal $1		sender/recipient common
R:; <@>			$@				list:; special case

# do special header rewriting
R$* <@> $*		$@ $1 <@> $2			pass null host through
R< @ $* > $*		$@ < @ $1 > $2			pass route-addr through
R$*			$: $>MasqSMTP $1		qualify unqual'ed names
R$+			$: $>MasqHdr $1			do masquerading


#
#  relay mailer header masquerading recipient rewriting
#
SMasqRelay
R$+			$: $>MasqSMTP $1
R$+			$: $>MasqHdr $1

Msmtp,		P=[IPC], F=mDFMuX, S=EnvFromSMTP/HdrFromSMTP, R=EnvToSMTP, E=\r\n, L=990,
		T=DNS/RFC822/SMTP,
		A=TCP $h
Mesmtp,		P=[IPC], F=mDFMuXa, S=EnvFromSMTP/HdrFromSMTP, R=EnvToSMTP, E=\r\n, L=990,
		T=DNS/RFC822/SMTP,
		A=TCP $h
Msmtp8,		P=[IPC], F=mDFMuX8, S=EnvFromSMTP/HdrFromSMTP, R=EnvToSMTP, E=\r\n, L=990,
		T=DNS/RFC822/SMTP,
		A=TCP $h
Mdsmtp,		P=[IPC], F=mDFMuXa%, S=EnvFromSMTP/HdrFromSMTP, R=EnvToSMTP, E=\r\n, L=990,
		T=DNS/RFC822/SMTP,
		A=TCP $h
Mrelay,		P=[IPC], F=mDFMuXa8, S=EnvFromSMTP/HdrFromSMTP, R=MasqSMTP, E=\r\n, L=2040,
		T=DNS/RFC822/SMTP,
		A=TCP $h


######################*****##############
###   PROCMAIL Mailer specification   ###
##################*****##################

#####  $Id: procmail.m4,v 8.22 2001/11/12 23:11:34 ca Exp $  #####

Mprocmail,	P=/usr/bin/procmail, F=DFMSPhnu9, S=EnvFromSMTP/HdrFromSMTP, R=EnvToSMTP/HdrFromSMTP,
		T=DNS/RFC822/X-Unix,
		A=procmail -Y -m $h $f $u


##################################################
###   Local and Program Mailer specification   ###
##################################################

#####  $Id: local.m4,v 8.59 2004/11/23 00:37:25 ca Exp $  #####

#
#  Envelope sender rewriting
#
SEnvFromL
R<@>			$n			errors to mailer-daemon
R@ <@ $*>		$n			temporarily bypass Sun bogosity
R$+			$: $>AddDomain $1	add local domain if needed
R$*			$: $>MasqEnv $1		do masquerading

#
#  Envelope recipient rewriting
#
SEnvToL
R$+ < @ $* >		$: $1			strip host part

#
#  Header sender rewriting
#
SHdrFromL
R<@>			$n			errors to mailer-daemon
R@ <@ $*>		$n			temporarily bypass Sun bogosity
R$+			$: $>AddDomain $1	add local domain if needed
R$*			$: $>MasqHdr $1		do masquerading

#
#  Header recipient rewriting
#
SHdrToL
R$+			$: $>AddDomain $1	add local domain if needed
R$* < @ *LOCAL* > $*	$: $1 < @ $j . > $2

#
#  Common code to add local domain name (only if always-add-domain)
#
SAddDomain
R$* < @ $* > $* 	$@ $1 < @ $2 > $3	already fully qualified

R$+			$@ $1 < @ *LOCAL* >	add local qualification

Mlocal,		P=/usr/bin/procmail, F=lsDFMAw5:/|@qSPfhn9, S=EnvFromL/HdrFromL, R=EnvToL/HdrToL,
		T=DNS/RFC822/X-Unix,
		A=procmail -t -Y -a $h -d $u
Mprog,		P=/usr/sbin/smrsh, F=lsDFMoqeu9, S=EnvFromL/HdrFromL, R=EnvToL/HdrToL, D=$z:/,
		T=X-Unix/X-Unix/X-Unix,
		A=smrsh -c $u
'''
    with open("/etc/mail/sendmail.cf","w+") as f:
        f.write(sendmail_config)
    Service("sendmail","restart")
    Auto_Enable("sendmail","on")


def apache_configure(virtualhostname, webroot, ssl):
    os.system("yum install httpd -y ; yum install mod_ssl -y ; yum install openssl -y")
    httpd_ssl_config = '''
#
# This is the Apache server configuration file providing SSL support.
# It contains the configuration directives to instruct the server how to
# serve pages over an https connection. For detailing information about these 
# directives see <URL:http://httpd.apache.org/docs/2.2/mod/mod_ssl.html>
# 
# Do NOT simply read the instructions in here without understanding
# what they do.  They're here only as hints or reminders.  If you are unsure
# consult the online docs. You have been warned.  
#

LoadModule ssl_module modules/mod_ssl.so

#
# When we also provide SSL we have to listen to the 
# the HTTPS port in addition.
#
Listen 443

##
##  SSL Global Context
##
##  All SSL configuration in this context applies both to
##  the main server and all SSL-enabled virtual hosts.
##

#   Pass Phrase Dialog:
#   Configure the pass phrase gathering process.
#   The filtering dialog program (`builtin' is a internal
#   terminal dialog) has to provide the pass phrase on stdout.
SSLPassPhraseDialog  builtin

#   Inter-Process Session Cache:
#   Configure the SSL Session Cache: First the mechanism 
#   to use and second the expiring timeout (in seconds).
SSLSessionCache         shmcb:/var/cache/mod_ssl/scache(512000)
SSLSessionCacheTimeout  300

#   Semaphore:
#   Configure the path to the mutual exclusion semaphore the
#   SSL engine uses internally for inter-process synchronization. 
SSLMutex default

#   Pseudo Random Number Generator (PRNG):
#   Configure one or more sources to seed the PRNG of the 
#   SSL library. The seed data should be of good random quality.
#   WARNING! On some platforms /dev/random blocks if not enough entropy
#   is available. This means you then cannot use the /dev/random device
#   because it would lead to very long connection times (as long as
#   it requires to make more entropy available). But usually those
#   platforms additionally provide a /dev/urandom device which doesn't
#   block. So, if available, use this one instead. Read the mod_ssl User
#   Manual for more details.
SSLRandomSeed startup file:/dev/urandom  256
SSLRandomSeed connect builtin
#SSLRandomSeed startup file:/dev/random  512
#SSLRandomSeed connect file:/dev/random  512
#SSLRandomSeed connect file:/dev/urandom 512

#
# Use "SSLCryptoDevice" to enable any supported hardware
# accelerators. Use "openssl engine -v" to list supported
# engine names.  NOTE: If you enable an accelerator and the
# server does not start, consult the error logs and ensure
# your accelerator is functioning properly. 
#
SSLCryptoDevice builtin
#SSLCryptoDevice ubsec

##
## SSL Virtual Host Context
##

<VirtualHost _default_:443>

# General setup for the virtual host, inherited from global configuration
DocumentRoot "''' + webroot + '''"
ServerName ''' + virtualhostname + ''':443

# Use separate log files for the SSL virtual host; note that LogLevel
# is not inherited from httpd.conf.
ErrorLog logs/ssl_error_log
TransferLog logs/ssl_access_log
LogLevel warn

#   SSL Engine Switch:
#   Enable/Disable SSL for this virtual host.
SSLEngine on

#   SSL Protocol support:
# List the enable protocol levels with which clients will be able to
# connect.  Disable SSLv2 access by default:
SSLProtocol all -SSLv2

#   SSL Cipher Suite:
# List the ciphers that the client is permitted to negotiate.
# See the mod_ssl documentation for a complete list.
SSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW

#   Server Certificate:
# Point SSLCertificateFile at a PEM encoded certificate.  If
# the certificate is encrypted, then you will be prompted for a
# pass phrase.  Note that a kill -HUP will prompt again.  A new
# certificate can be generated using the genkey(1) command.
SSLCertificateFile /etc/pki/tls/certs/localhost.crt

#   Server Private Key:
#   If the key is not combined with the certificate, use this
#   directive to point at the key file.  Keep in mind that if
#   you've both a RSA and a DSA private key you can configure
#   both in parallel (to also allow the use of DSA ciphers, etc.)
SSLCertificateKeyFile /etc/pki/tls/private/localhost.key

#   Server Certificate Chain:
#   Point SSLCertificateChainFile at a file containing the
#   concatenation of PEM encoded CA certificates which form the
#   certificate chain for the server certificate. Alternatively
#   the referenced file can be the same as SSLCertificateFile
#   when the CA certificates are directly appended to the server
#   certificate for convinience.
#SSLCertificateChainFile /etc/pki/tls/certs/server-chain.crt

#   Certificate Authority (CA):
#   Set the CA certificate verification path where to find CA
#   certificates for client authentication or alternatively one
#   huge file containing all of them (file must be PEM encoded)
#SSLCACertificateFile /etc/pki/tls/certs/ca-bundle.crt

#   Client Authentication (Type):
#   Client certificate verification type and depth.  Types are
#   none, optional, require and optional_no_ca.  Depth is a
#   number which specifies how deeply to verify the certificate
#   issuer chain before deciding the certificate is not valid.
#SSLVerifyClient require
#SSLVerifyDepth  10

#   Access Control:
#   With SSLRequire you can do per-directory access control based
#   on arbitrary complex boolean expressions containing server
#   variable checks and other lookup directives.  The syntax is a
#   mixture between C and Perl.  See the mod_ssl documentation
#   for more details.
#<Location />
#SSLRequire (    %{SSL_CIPHER} !~ m/^(EXP|NULL)/ \
#            and %{SSL_CLIENT_S_DN_O} eq "Snake Oil, Ltd." \
#            and %{SSL_CLIENT_S_DN_OU} in {"Staff", "CA", "Dev"} \
#            and %{TIME_WDAY} >= 1 and %{TIME_WDAY} <= 5 \
#            and %{TIME_HOUR} >= 8 and %{TIME_HOUR} <= 20       ) \
#           or %{REMOTE_ADDR} =~ m/^192\.76\.162\.[0-9]+$/
#</Location>

#   SSL Engine Options:
#   Set various options for the SSL engine.
#   o FakeBasicAuth:
#     Translate the client X.509 into a Basic Authorisation.  This means that
#     the standard Auth/DBMAuth methods can be used for access control.  The
#     user name is the `one line' version of the client's X.509 certificate.
#     Note that no password is obtained from the user. Every entry in the user
#     file needs this password: `xxj31ZMTZzkVA'.
#   o ExportCertData:
#     This exports two additional environment variables: SSL_CLIENT_CERT and
#     SSL_SERVER_CERT. These contain the PEM-encoded certificates of the
#     server (always existing) and the client (only existing when client
#     authentication is used). This can be used to import the certificates
#     into CGI scripts.
#   o StdEnvVars:
#     This exports the standard SSL/TLS related `SSL_*' environment variables.
#     Per default this exportation is switched off for performance reasons,
#     because the extraction step is an expensive operation and is usually
#     useless for serving static content. So one usually enables the
#     exportation for CGI and SSI requests only.
#   o StrictRequire:
#     This denies access when "SSLRequireSSL" or "SSLRequire" applied even
#     under a "Satisfy any" situation, i.e. when it applies access is denied
#     and no other module can change it.
#   o OptRenegotiate:
#     This enables optimized SSL connection renegotiation handling when SSL
#     directives are used in per-directory context. 
#SSLOptions +FakeBasicAuth +ExportCertData +StrictRequire
<Files ~ "\.(cgi|shtml|phtml|php3?)$">
    SSLOptions +StdEnvVars
</Files>
<Directory "/var/www/cgi-bin">
    SSLOptions +StdEnvVars
</Directory>

#   SSL Protocol Adjustments:
#   The safe and default but still SSL/TLS standard compliant shutdown
#   approach is that mod_ssl sends the close notify alert but doesn't wait for
#   the close notify alert from client. When you need a different shutdown
#   approach you can use one of the following variables:
#   o ssl-unclean-shutdown:
#     This forces an unclean shutdown when the connection is closed, i.e. no
#     SSL close notify alert is send or allowed to received.  This violates
#     the SSL/TLS standard but is needed for some brain-dead browsers. Use
#     this when you receive I/O errors because of the standard approach where
#     mod_ssl sends the close notify alert.
#   o ssl-accurate-shutdown:
#     This forces an accurate shutdown when the connection is closed, i.e. a
#     SSL close notify alert is send and mod_ssl waits for the close notify
#     alert of the client. This is 100% SSL/TLS standard compliant, but in
#     practice often causes hanging connections with brain-dead browsers. Use
#     this only for browsers where you know that their SSL implementation
#     works correctly. 
#   Notice: Most problems of broken clients are also related to the HTTP
#   keep-alive facility, so you usually additionally want to disable
#   keep-alive for those clients, too. Use variable "nokeepalive" for this.
#   Similarly, one has to force some clients to use HTTP/1.0 to workaround
#   their broken HTTP/1.1 implementation. Use variables "downgrade-1.0" and
#   "force-response-1.0" for this.
SetEnvIf User-Agent ".*MSIE.*" \
         nokeepalive ssl-unclean-shutdown \
         downgrade-1.0 force-response-1.0

#   Per-Server Logging:
#   The home of a custom SSL log file. Use this when you want a
#   compact non-error SSL logfile on a virtual host basis.

</VirtualHost>                                  
'''
    apache_httpd_config = '''
<VirtualHost *:80>
    #ServerAdmin webmaster@dummy-host.example.com
    DocumentRoot ''' + webroot + '''
    ServerName ''' + virtualhostname + '''
    ErrorLog logs/dummy-host.example.com-error_log
    CustomLog logs/dummy-host.example.com-access_log common
</VirtualHost>
'''
    if ssl == 'yes':
        with open("/etc/httpd/conf.d/ssl.conf", "w+") as f:
            f.write(httpd_ssl_config)
    else:
        with open("/etc/httpd/conf/httpd.conf", "a") as f:
            f.write(apache_httpd_config)
    Service("httpd","restart")
    Auto_Enable("httpd", "on")

def Unbound_configure():
    os.system("yum install unbound -y")
    unbound_config = """
#
# See unbound.conf(5) man page.
#
# this is a comment.

#Use this to include other text into the file.
#include: "otherfile.conf"

# The server clause sets the main parameters.
server:
	# whitespace is not necessary, but looks cleaner.

	# verbosity number, 0 is least verbose. 1 is default.
	verbosity: 1

	# print statistics to the log (for every thread) every N seconds.
	# Set to "" or 0 to disable. Default is disabled.
	# Needs to be disabled for munin plugin
	statistics-interval: 0

	# enable shm for stats, default no.  if you enable also enable
	# statistics-interval, every time it also writes stats to the
	# shared memory segment keyed with shm-key.
	# shm-enable: no

	# shm for stats uses this key, and key+1 for the shared mem segment.
	# shm-key: 11777

	# enable cumulative statistics, without clearing them after printing.
	# Needs to be disabled for munin plugin
	statistics-cumulative: no

	# enable extended statistics (query types, answer codes, status)
	# printed from unbound-control. default off, because of speed.
	# Needs to be enabled for munin plugin
	extended-statistics: yes

	# number of threads to create. 1 disables threading.
	num-threads: 4

	# specify the interfaces to answer queries from by ip-address.
	# The default is to listen to localhost (127.0.0.1 and ::1).
	# specify 0.0.0.0 and ::0 to bind to all available interfaces.
	# specify every interface[@port] on a new 'interface:' labelled line.
	# The listen interfaces are not changed on reload, only on restart.
	interface: 0.0.0.0
	# interface: ::0
	# interface: 192.0.2.153
	# interface: 192.0.2.154
	# interface: 192.0.2.154@5003
	# interface: 2001:DB8::5
	#
	# for dns over tls and raw dns over port 80
	# interface: 0.0.0.0@443
	# interface: ::0@443
	# interface: 0.0.0.0@80
	# interface: ::0@80

	# enable this feature to copy the source address of queries to reply.
	# Socket options are not supported on all platforms. experimental.
	# interface-automatic: yes
	#
	# NOTE: Enable this option when specifying interface 0.0.0.0 or ::0
	# NOTE: Disabled per Fedora policy not to listen to * on default install
	# NOTE: If deploying on non-default port, eg 80/443, this needs to be disabled
	interface-automatic: no

	# port to answer queries from
	# port: 53

	# specify the interfaces to send outgoing queries to authoritative
	# server from by ip-address. If none, the default (all) interface
	# is used. Specify every interface on a 'outgoing-interface:' line.
	# outgoing-interface: 192.0.2.153
	# outgoing-interface: 2001:DB8::5
	# outgoing-interface: 2001:DB8::6

	# Specify a netblock to use remainder 64 bits as random bits for
	# upstream queries.  Uses freebind option (Linux).
	# outgoing-interface: 2001:DB8::/64
	# Also (Linux:) ip -6 addr add 2001:db8::/64 dev lo
	# And: ip -6 route add local 2001:db8::/64 dev lo
	# And set prefer-ip6: yes to use the ip6 randomness from a netblock.
	# Set this to yes to prefer ipv6 upstream servers over ipv4.
	# prefer-ip6: no

	# number of ports to allocate per thread, determines the size of the
	# port range that can be open simultaneously.  About double the
	# num-queries-per-thread, or, use as many as the OS will allow you.
	# outgoing-range: 4096

	# permit unbound to use this port number or port range for
	# making outgoing queries, using an outgoing interface.
	# outgoing-port-permit: 32768-65535

	# deny unbound the use this of port number or port range for
	# making outgoing queries, using an outgoing interface.
	# Use this to make sure unbound does not grab a UDP port that some
	# other server on this computer needs. The default is to avoid
	# IANA-assigned port numbers.
	# If multiple outgoing-port-permit and outgoing-port-avoid options
	# are present, they are processed in order.
	# outgoing-port-avoid: 0-32767

	# number of outgoing simultaneous tcp buffers to hold per thread.
	# outgoing-num-tcp: 10

	# number of incoming simultaneous tcp buffers to hold per thread.
	# incoming-num-tcp: 10

	# buffer size for UDP port 53 incoming (SO_RCVBUF socket option).
	# 0 is system default.  Use 4m to catch query spikes for busy servers.
	# so-rcvbuf: 0

	# buffer size for UDP port 53 outgoing (SO_SNDBUF socket option).
	# 0 is system default.  Use 4m to handle spikes on very busy servers.
	# so-sndbuf: 0

	# use SO_REUSEPORT to distribute queries over threads.
	so-reuseport: yes

	# use IP_TRANSPARENT so the interface: addresses can be non-local
	# and you can config non-existing IPs that are going to work later on
	# (uses IP_BINDANY on FreeBSD).
	ip-transparent: yes

	# use IP_FREEBIND so the interface: addresses can be non-local
	# and you can bind to nonexisting IPs and interfaces that are down.
	# Linux only.  On Linux you also have ip-transparent that is similar.
	# ip-freebind: no

	# EDNS reassembly buffer to advertise to UDP peers (the actual buffer
	# is set with msg-buffer-size). 1472 can solve fragmentation (timeouts).
	# edns-buffer-size: 4096

	# Maximum UDP response size (not applied to TCP response).
	# Suggested values are 512 to 4096. Default is 4096. 65536 disables it.
	# 3072 causes +dnssec any isc.org queries to need TC=1.
	# Helps mitigating DDOS
	# max-udp-size: 3072

	# buffer size for handling DNS data. No messages larger than this
	# size can be sent or received, by UDP or TCP. In bytes.
	# msg-buffer-size: 65552

	# the amount of memory to use for the message cache.
	# plain value in bytes or you can append k, m or G. default is "4Mb".
	# msg-cache-size: 4m

	# the number of slabs to use for the message cache.
	# the number of slabs must be a power of 2.
	# more slabs reduce lock contention, but fragment memory usage.
	# msg-cache-slabs: 4

	# the number of queries that a thread gets to service.
	# num-queries-per-thread: 1024

	# if very busy, 50% queries run to completion, 50% get timeout in msec
	# jostle-timeout: 200

	# msec to wait before close of port on timeout UDP. 0 disables.
	# delay-close: 0

	# the amount of memory to use for the RRset cache.
	# plain value in bytes or you can append k, m or G. default is "4Mb".
	# rrset-cache-size: 4m

	# the number of slabs to use for the RRset cache.
	# the number of slabs must be a power of 2.
	# more slabs reduce lock contention, but fragment memory usage.
	# rrset-cache-slabs: 4

	# the time to live (TTL) value lower bound, in seconds. Default 0.
	# If more than an hour could easily give trouble due to stale data.
	# cache-min-ttl: 0

	# the time to live (TTL) value cap for RRsets and messages in the
	# cache. Items are not cached for longer. In seconds.
	# cache-max-ttl: 86400

	# the time to live (TTL) value cap for negative responses in the cache
	# cache-max-negative-ttl: 3600

	# the time to live (TTL) value for cached roundtrip times, lameness and
	# EDNS version information for hosts. In seconds.
	# infra-host-ttl: 900

	# minimum wait time for responses, increase if uplink is long. In msec.
	# infra-cache-min-rtt: 50

	# the number of slabs to use for the Infrastructure cache.
	# the number of slabs must be a power of 2.
	# more slabs reduce lock contention, but fragment memory usage.
	# infra-cache-slabs: 4

	# the maximum number of hosts that are cached (roundtrip, EDNS, lame).
	# infra-cache-numhosts: 10000

	# define a number of tags here, use with local-zone, access-control.
	# repeat the define-tag statement to add additional tags.
	# define-tag: "tag1 tag2 tag3"

	# Enable IPv4, "yes" or "no".
	# do-ip4: yes

	# Enable IPv6, "yes" or "no".
	# do-ip6: yes

	# Enable UDP, "yes" or "no".
	# NOTE: if setting up an unbound on tls443 for public use, you might want to
	# disable UDP to avoid being used in DNS amplification attacks.
	# do-udp: yes

	# Enable TCP, "yes" or "no".
	# do-tcp: yes

	# upstream connections use TCP only (and no UDP), "yes" or "no"
	# useful for tunneling scenarios, default no.
	# tcp-upstream: no

	# Maximum segment size (MSS) of TCP socket on which the server
	# responds to queries. Default is 0, system default MSS.
	# tcp-mss: 0

	# Maximum segment size (MSS) of TCP socket for outgoing queries.
	# Default is 0, system default MSS.
	# outgoing-tcp-mss: 0

	# Detach from the terminal, run in background, "yes" or "no".
	# Set the value to "no" when unbound runs as systemd service.
	# do-daemonize: yes

	# control which clients are allowed to make (recursive) queries
	# to this server. Specify classless netblocks with /size and action.
	# By default everything is refused, except for localhost.
	# Choose deny (drop message), refuse (polite error reply),
	# allow (recursive ok), allow_snoop (recursive and nonrecursive ok)
	# deny_non_local (drop queries unless can be answered from local-data)
	# refuse_non_local (like deny_non_local but polite error reply).
	access-control: 0.0.0.0/0 allow
	# access-control: 127.0.0.0/8 allow
	# access-control: ::0/0 refuse
	# access-control: ::1 allow
	# access-control: ::ffff:127.0.0.1 allow

	# tag access-control with list of tags (in "" with spaces between)
	# Clients using this access control element use localzones that
	# are tagged with one of these tags.
	# access-control-tag: 192.0.2.0/24 "tag2 tag3"

	# set action for particular tag for given access control element
	# if you have multiple tag values, the tag used to lookup the action
	# is the first tag match between access-control-tag and local-zone-tag
	# where "first" comes from the order of the define-tag values.
	# access-control-tag-action: 192.0.2.0/24 tag3 refuse

	# set redirect data for particular tag for access control element
	# access-control-tag-data: 192.0.2.0/24 tag2 "A 127.0.0.1"

	# Set view for access control element
	# access-control-view: 192.0.2.0/24 viewname

	# if given, a chroot(2) is done to the given directory.
	# i.e. you can chroot to the working directory, for example,
	# for extra security, but make sure all files are in that directory.
	#
	# If chroot is enabled, you should pass the configfile (from the
	# commandline) as a full path from the original root. After the
	# chroot has been performed the now defunct portion of the config
	# file path is removed to be able to reread the config after a reload.
	#
	# All other file paths (working dir, logfile, roothints, and
	# key files) can be specified in several ways:
	# 	o as an absolute path relative to the new root.
	# 	o as a relative path to the working directory.
	# 	o as an absolute path relative to the original root.
	# In the last case the path is adjusted to remove the unused portion.
	#
	# The pid file can be absolute and outside of the chroot, it is
	# written just prior to performing the chroot and dropping permissions.
	#
	# Additionally, unbound may need to access /dev/random (for entropy).
	# How to do this is specific to your OS.
	#
	# If you give "" no chroot is performed. The path must not end in a /.
	# chroot: "/var/lib/unbound"
	chroot: ""

	# if given, user privileges are dropped (after binding port),
	# and the given username is assumed. Default is user "unbound".
	# If you give "" no privileges are dropped.
	username: ""

	# the working directory. The relative files in this config are
	# relative to this directory. If you give "" the working directory
	# is not changed.
	# If you give a server: directory: dir before include: file statements
	# then those includes can be relative to the working directory.
	directory: "/etc/unbound"

	# the log file, "" means log to stderr.
	# Use of this option sets use-syslog to "no".
	# logfile: ""

	# Log to syslog(3) if yes. The log facility LOG_DAEMON is used to
	# log to, with identity "unbound". If yes, it overrides the logfile.
	# use-syslog: yes
 
	# Log identity to report. if empty, defaults to the name of argv[0]
	# (usually "unbound").
	# log-identity: ""

	# print UTC timestamp in ascii to logfile, default is epoch in seconds.
	log-time-ascii: yes

	# print one line with time, IP, name, type, class for every query.
	# log-queries: no

	# print one line per reply, with time, IP, name, type, class, rcode,
	# timetoresolve, fromcache and responsesize.
	# log-replies: no

	# the pid file. Can be an absolute path outside of chroot/work dir.
	pidfile: "/var/run/unbound/unbound.pid"

	# file to read root hints from.
	# get one from https://www.internic.net/domain/named.cache
	# root-hints: ""

	# enable to not answer id.server and hostname.bind queries.
	# hide-identity: no

	# enable to not answer version.server and version.bind queries.
	# hide-version: no

	# enable to not answer trustanchor.unbound queries.
	# hide-trustanchor: no

	# the identity to report. Leave "" or default to return hostname.
	# identity: ""

	# the version to report. Leave "" or default to return package version.
	# version: ""

	# the target fetch policy.
	# series of integers describing the policy per dependency depth.
	# The number of values in the list determines the maximum dependency
	# depth the recursor will pursue before giving up. Each integer means:
	# 	-1 : fetch all targets opportunistically,
	# 	0: fetch on demand,
	#	positive value: fetch that many targets opportunistically.
	# Enclose the list of numbers between quotes ("").
	# target-fetch-policy: "3 2 1 0 0"

	# Harden against very small EDNS buffer sizes.
	# harden-short-bufsize: no

	# Harden against unseemly large queries.
	# harden-large-queries: no

	# Harden against out of zone rrsets, to avoid spoofing attempts.
	harden-glue: yes

	# Harden against receiving dnssec-stripped data. If you turn it
	# off, failing to validate dnskey data for a trustanchor will
	# trigger insecure mode for that zone (like without a trustanchor).
	# Default on, which insists on dnssec data for trust-anchored zones.
	harden-dnssec-stripped: yes

	# Harden against queries that fall under dnssec-signed nxdomain names.
	harden-below-nxdomain: yes

	# Harden the referral path by performing additional queries for
	# infrastructure data.  Validates the replies (if possible).
	# Default off, because the lookups burden the server.  Experimental
	# implementation of draft-wijngaards-dnsext-resolver-side-mitigation.
	harden-referral-path: yes

	# Harden against algorithm downgrade when multiple algorithms are
	# advertised in the DS record.  If no, allows the weakest algorithm
	# to validate the zone.
	# harden-algo-downgrade: no

	# Sent minimum amount of information to upstream servers to enhance
	# privacy. Only sent minimum required labels of the QNAME and set QTYPE
	# to NS when possible.
	# qname-minimisation: no

	# QNAME minimisation in strict mode. Do not fall-back to sending full
	# QNAME to potentially broken nameservers. A lot of domains will not be
	# resolvable when this option in enabled.
	# This option only has effect when qname-minimisation is enabled.
	# qname-minimisation-strict: no

	# Use 0x20-encoded random bits in the query to foil spoof attempts.
	# This feature is an experimental implementation of draft dns-0x20.
	# use-caps-for-id: no

	# Domains (and domains in them) without support for dns-0x20 and
	# the fallback fails because they keep sending different answers.
	# caps-whitelist: "licdn.com"
	# caps-whitelist: "senderbase.org"

	# Enforce privacy of these addresses. Strips them away from answers.
	# It may cause DNSSEC validation to additionally mark it as bogus.
	# Protects against 'DNS Rebinding' (uses browser as network proxy).
	# Only 'private-domain' and 'local-data' names are allowed to have
	# these private addresses. No default.
	# private-address: 10.0.0.0/8
	# private-address: 172.16.0.0/12
	# private-address: 192.168.0.0/16
	# private-address: 169.254.0.0/16
	# private-address: fd00::/8
	# private-address: fe80::/10
	# private-address: ::ffff:0:0/96

	# Allow the domain (and its subdomains) to contain private addresses.
	# local-data statements are allowed to contain private addresses too.
	# private-domain: "example.com"

	# If nonzero, unwanted replies are not only reported in statistics,
	# but also a running total is kept per thread. If it reaches the
	# threshold, a warning is printed and a defensive action is taken,
	# the cache is cleared to flush potential poison out of it.
	# A suggested value is 10000000, the default is 0 (turned off).
	unwanted-reply-threshold: 10000000

	# Do not query the following addresses. No DNS queries are sent there.
	# List one address per entry. List classless netblocks with /size,
	# do-not-query-address: 127.0.0.1/8
	# do-not-query-address: ::1

	# if yes, the above default do-not-query-address entries are present.
	# if no, localhost can be queried (for testing and debugging).
	# do-not-query-localhost: yes

	# if yes, perform prefetching of almost expired message cache entries.
	prefetch: yes

	# if yes, perform key lookups adjacent to normal lookups.
	prefetch-key: yes

	# if yes, Unbound rotates RRSet order in response.
	rrset-roundrobin: yes

	# if yes, Unbound doesn't insert authority/additional sections
	# into response messages when those sections are not required.
	minimal-responses: yes

	# true to disable DNSSEC lameness check in iterator.
	# disable-dnssec-lame-check: no

	# module configuration of the server. A string with identifiers
	# separated by spaces. Syntax: "[dns64] [validator] iterator"
	# module-config: "validator iterator"
	module-config: "ipsecmod validator iterator"

	# File with trusted keys, kept uptodate using RFC5011 probes,
	# initial file like trust-anchor-file, then it stores metadata.
	# Use several entries, one per domain name, to track multiple zones.
	#
	# If you want to perform DNSSEC validation, run unbound-anchor before
	# you start unbound (i.e. in the system boot scripts).  And enable:
	# Please note usage of unbound-anchor root anchor is at your own risk
	# and under the terms of our LICENSE (see that file in the source).
	# auto-trust-anchor-file: "/var/lib/unbound/root.key"

	# trust anchor signaling sends a RFC8145 key tag query after priming.
	trust-anchor-signaling: yes

	# File with DLV trusted keys. Same format as trust-anchor-file.
	# There can be only one DLV configured, it is trusted from root down.
	# DLV is going to be decommissioned.  Please do not use it any more.
	# dlv-anchor-file: "dlv.isc.org.key"

	# File with trusted keys for validation. Specify more than one file
	# with several entries, one file per entry.
	# Zone file format, with DS and DNSKEY entries.
	# Note this gets out of date, use auto-trust-anchor-file please.
	# trust-anchor-file: ""

	# Trusted key for validation. DS or DNSKEY. specify the RR on a
	# single line, surrounded by "". TTL is ignored. class is IN default.
	# Note this gets out of date, use auto-trust-anchor-file please.
	# (These examples are from August 2007 and may not be valid anymore).
	# trust-anchor: "nlnetlabs.nl. DNSKEY 257 3 5 AQPzzTWMz8qSWIQlfRnPckx2BiVmkVN6LPupO3mbz7FhLSnm26n6iG9N Lby97Ji453aWZY3M5/xJBSOS2vWtco2t8C0+xeO1bc/d6ZTy32DHchpW 6rDH1vp86Ll+ha0tmwyy9QP7y2bVw5zSbFCrefk8qCUBgfHm9bHzMG1U BYtEIQ=="
	# trust-anchor: "jelte.nlnetlabs.nl. DS 42860 5 1 14D739EB566D2B1A5E216A0BA4D17FA9B038BE4A"

	# File with trusted keys for validation. Specify more than one file
	# with several entries, one file per entry. Like trust-anchor-file
	# but has a different file format. Format is BIND-9 style format,
	# the trusted-keys { name flag proto algo "key"; }; clauses are read.
	# you need external update procedures to track changes in keys.
	# trusted-keys-file: ""
	#
	trusted-keys-file: /etc/unbound/keys.d/*.key
	auto-trust-anchor-file: "/var/lib/unbound/root.key"

	# Ignore chain of trust. Domain is treated as insecure.
	# domain-insecure: "example.com"

	# Override the date for validation with a specific fixed date.
	# Do not set this unless you are debugging signature inception
	# and expiration. "" or "0" turns the feature off. -1 ignores date.
	# val-override-date: ""

	# The time to live for bogus data, rrsets and messages. This avoids
	# some of the revalidation, until the time interval expires. in secs.
	# val-bogus-ttl: 60

	# The signature inception and expiration dates are allowed to be off
	# by 10% of the signature lifetime (expir-incep) from our local clock.
	# This leeway is capped with a minimum and a maximum.  In seconds.
	# val-sig-skew-min: 3600
	# val-sig-skew-max: 86400

	# Should additional section of secure message also be kept clean of
	# unsecure data. Useful to shield the users of this validator from
	# potential bogus data in the additional section. All unsigned data
	# in the additional section is removed from secure messages.
	val-clean-additional: yes

	# Turn permissive mode on to permit bogus messages. Thus, messages
	# for which security checks failed will be returned to clients,
	# instead of SERVFAIL. It still performs the security checks, which
	# result in interesting log files and possibly the AD bit in
	# replies if the message is found secure. The default is off.
	# NOTE: TURNING THIS ON DISABLES ALL DNSSEC SECURITY
	val-permissive-mode: no

	# Ignore the CD flag in incoming queries and refuse them bogus data.
	# Enable it if the only clients of unbound are legacy servers (w2008)
	# that set CD but cannot validate themselves.
	# ignore-cd-flag: no

	# Serve expired responses from cache, with TTL 0 in the response,
	# and then attempt to fetch the data afresh.
	# serve-expired: no

	# Have the validator log failed validations for your diagnosis.
	# 0: off. 1: A line per failed user query. 2: With reason and bad IP.
	val-log-level: 1

	# It is possible to configure NSEC3 maximum iteration counts per
	# keysize. Keep this table very short, as linear search is done.
	# A message with an NSEC3 with larger count is marked insecure.
	# List in ascending order the keysize and count values.
	# val-nsec3-keysize-iterations: "1024 150 2048 500 4096 2500"

	# instruct the auto-trust-anchor-file probing to add anchors after ttl.
	# add-holddown: 2592000 # 30 days

	# instruct the auto-trust-anchor-file probing to del anchors after ttl.
	# del-holddown: 2592000 # 30 days

	# auto-trust-anchor-file probing removes missing anchors after ttl.
	# If the value 0 is given, missing anchors are not removed.
	# keep-missing: 31622400 # 366 days

	# debug option that allows very small holddown times for key rollover,
	# otherwise the RFC mandates probe intervals must be at least 1 hour.
	# permit-small-holddown: no

	# the amount of memory to use for the key cache.
	# plain value in bytes or you can append k, m or G. default is "4Mb".
	# key-cache-size: 4m

	# the number of slabs to use for the key cache.
	# the number of slabs must be a power of 2.
	# more slabs reduce lock contention, but fragment memory usage.
	# key-cache-slabs: 4

	# the amount of memory to use for the negative cache (used for DLV).
	# plain value in bytes or you can append k, m or G. default is "1Mb".
	# neg-cache-size: 1m

	# By default, for a number of zones a small default 'nothing here'
	# reply is built-in.  Query traffic is thus blocked.  If you
	# wish to serve such zone you can unblock them by uncommenting one
	# of the nodefault statements below.
	# You may also have to use domain-insecure: zone to make DNSSEC work,
	# unless you have your own trust anchors for this zone.
	# local-zone: "localhost." nodefault
	# local-zone: "127.in-addr.arpa." nodefault
	# local-zone: "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa." nodefault
	# local-zone: "onion." nodefault
	# local-zone: "test." nodefault
	# local-zone: "invalid." nodefault
	# local-zone: "10.in-addr.arpa." nodefault
	# local-zone: "16.172.in-addr.arpa." nodefault
	# local-zone: "17.172.in-addr.arpa." nodefault
	# local-zone: "18.172.in-addr.arpa." nodefault
	# local-zone: "19.172.in-addr.arpa." nodefault
	# local-zone: "20.172.in-addr.arpa." nodefault
	# local-zone: "21.172.in-addr.arpa." nodefault
	# local-zone: "22.172.in-addr.arpa." nodefault
	# local-zone: "23.172.in-addr.arpa." nodefault
	# local-zone: "24.172.in-addr.arpa." nodefault
	# local-zone: "25.172.in-addr.arpa." nodefault
	# local-zone: "26.172.in-addr.arpa." nodefault
	# local-zone: "27.172.in-addr.arpa." nodefault
	# local-zone: "28.172.in-addr.arpa." nodefault
	# local-zone: "29.172.in-addr.arpa." nodefault
	# local-zone: "30.172.in-addr.arpa." nodefault
	# local-zone: "31.172.in-addr.arpa." nodefault
	# local-zone: "168.192.in-addr.arpa." nodefault
	# local-zone: "0.in-addr.arpa." nodefault
	# local-zone: "254.169.in-addr.arpa." nodefault
	# local-zone: "2.0.192.in-addr.arpa." nodefault
	# local-zone: "100.51.198.in-addr.arpa." nodefault
	# local-zone: "113.0.203.in-addr.arpa." nodefault
	# local-zone: "255.255.255.255.in-addr.arpa." nodefault
	# local-zone: "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa." nodefault
	# local-zone: "d.f.ip6.arpa." nodefault
	# local-zone: "8.e.f.ip6.arpa." nodefault
	# local-zone: "9.e.f.ip6.arpa." nodefault
	# local-zone: "a.e.f.ip6.arpa." nodefault
	# local-zone: "b.e.f.ip6.arpa." nodefault
	# local-zone: "8.b.d.0.1.0.0.2.ip6.arpa." nodefault
	# And for 64.100.in-addr.arpa. to 127.100.in-addr.arpa.

	# If unbound is running service for the local host then it is useful
	# to perform lan-wide lookups to the upstream, and unblock the
	# long list of local-zones above.  If this unbound is a dns server
	# for a network of computers, disabled is better and stops information
	# leakage of local lan information.
	# unblock-lan-zones: no

	# The insecure-lan-zones option disables validation for
	# these zones, as if they were all listed as domain-insecure.
	# insecure-lan-zones: no

	# The insecure-lan-zones option disables validation for
	# these zones, as if they were all listed as domain-insecure.
	# insecure-lan-zones: no

	# a number of locally served zones can be configured.
	# 	local-zone: <zone> <type>
	# 	local-data: "<resource record string>"
	# o deny serves local data (if any), else, drops queries.
	# o refuse serves local data (if any), else, replies with error.
	# o static serves local data, else, nxdomain or nodata answer.
	# o transparent gives local data, but resolves normally for other names
	# o redirect serves the zone data for any subdomain in the zone.
	# o nodefault can be used to normally resolve AS112 zones.
	# o typetransparent resolves normally for other types and other names
	# o inform resolves normally, but logs client IP address
	# o inform_deny drops queries and logs client IP address
	# o always_transparent, always_refuse, always_nxdomain, resolve in
	#   that way but ignore local data for that name.
	#
	# defaults are localhost address, reverse for 127.0.0.1 and ::1
	# and nxdomain for AS112 zones. If you configure one of these zones
	# the default content is omitted, or you can omit it with 'nodefault'.
	#
	# If you configure local-data without specifying local-zone, by
	# default a transparent local-zone is created for the data.
	#
	# You can add locally served data with
	# local-zone: "local." static
	# local-data: "mycomputer.local. IN A 192.0.2.51"
	# local-data: 'mytext.local TXT "content of text record"'
	#
	# You can override certain queries with
	# local-data: "adserver.example.com A 127.0.0.1"
	#
	# You can redirect a domain to a fixed address with
	# (this makes example.com, www.example.com, etc, all go to 192.0.2.3)
	# local-zone: "example.com" redirect
	# local-data: "example.com A 192.0.2.3"
	#
	# Shorthand to make PTR records, "IPv4 name" or "IPv6 name".
	# You can also add PTR records using local-data directly, but then
	# you need to do the reverse notation yourself.
	# local-data-ptr: "192.0.2.3 www.example.com"

	include: /etc/unbound/local.d/*.conf

	# tag a localzone with a list of tag names (in "" with spaces between)
	# local-zone-tag: "example.com" "tag2 tag3"

	# add a netblock specific override to a localzone, with zone type
	# local-zone-override: "example.com" 192.0.2.0/24 refuse

	# service clients over SSL (on the TCP sockets), with plain DNS inside
	# the SSL stream.  Give the certificate to use and private key.
	# default is "" (disabled).  requires restart to take effect.
	# ssl-service-key: "/etc/unbound/unbound_server.key"
	# ssl-service-pem: "/etc/unbound/unbound_server.pem"
	# ssl-port: 443
	#
	# request upstream over SSL (with plain DNS inside the SSL stream).
	# Default is no.  Can be turned on and off with unbound-control.
	# ssl-upstream: no

	# DNS64 prefix. Must be specified when DNS64 is use.
	# Enable dns64 in module-config.  Used to synthesize IPv6 from IPv4.
	# dns64-prefix: 64:ff9b::0/96

	# ratelimit for uncached, new queries, this limits recursion effort.
	# ratelimiting is experimental, and may help against randomqueryflood.
	# if 0(default) it is disabled, otherwise state qps allowed per zone.
	# ratelimit: 0

	# ratelimits are tracked in a cache, size in bytes of cache (or k,m).
	# ratelimit-size: 4m
	# ratelimit cache slabs, reduces lock contention if equal to cpucount.
	# ratelimit-slabs: 4

	# 0 blocks when ratelimited, otherwise let 1/xth traffic through
	# ratelimit-factor: 10

	# override the ratelimit for a specific domain name.
	# give this setting multiple times to have multiple overrides.
	# ratelimit-for-domain: example.com 1000
	# override the ratelimits for all domains below a domain name
	# can give this multiple times, the name closest to the zone is used.
	# ratelimit-below-domain: com 1000

	# global query ratelimit for all ip addresses.
	# feature is experimental.
	# if 0(default) it is disabled, otherwise states qps allowed per ip address
	# ip-ratelimit: 0

	# ip ratelimits are tracked in a cache, size in bytes of cache (or k,m).
	# ip-ratelimit-size: 4m
	# ip ratelimit cache slabs, reduces lock contention if equal to cpucount.
	# ip-ratelimit-slabs: 4

	# 0 blocks when ip is ratelimited, otherwise let 1/xth traffic through
	# ip-ratelimit-factor: 10

	# Specific options for ipsecmod.
	#
	# Enable or disable ipsecmod (it still needs to be defined in
	# module-config above). Can be used when ipsecmod needs to be
	# enabled/disabled via remote-control(below).
	ipsecmod-enabled: no
	#
	# Path to executable external hook. It must be defined when ipsecmod is
	# listed in module-config (above).
	ipsecmod-hook: "/usr/libexec/ipsec/_unbound-hook"
	#
	# When enabled unbound will reply with SERVFAIL if the return value of
	# the ipsecmod-hook is not 0.
	# ipsecmod-strict: no
	#
	# Maximum time to live (TTL) for cached A/AAAA records with IPSECKEY.
	# ipsecmod-max-ttl: 3600
	#
	# Reply with A/AAAA even if the relevant IPSECKEY is bogus. Mainly used for
	# testing.
	# ipsecmod-ignore-bogus: no
	#
	# Domains for which ipsecmod will be triggered. If not defined (default)
	# all domains are treated as being whitelisted.
	# ipsecmod-whitelist: "example.com"
	# ipsecmod-whitelist: "nlnetlabs.nl"

# Python config section. To enable:
# o use --with-pythonmodule to configure before compiling.
# o list python in the module-config string (above) to enable.
# o and give a python-script to run.
python:
	# Script file to load
	# python-script: "/etc/unbound/ubmodule-tst.py"

# Remote control config section.
remote-control:
	# Enable remote control with unbound-control(8) here.
	# set up the keys and certificates with unbound-control-setup.
	# Note: required for unbound-munin package
	control-enable: yes

	# Set to no and use an absolute path as control-interface to use
	# a unix local named pipe for unbound-control.
	# control-use-cert: yes

	# what interfaces are listened to for remote control.
	# give 0.0.0.0 and ::0 to listen to all interfaces.
	# control-interface: 127.0.0.1
	# control-interface: ::1

	# port number for remote control operations.
	# control-port: 8953

	# unbound server key file.
	server-key-file: "/etc/unbound/unbound_server.key"

	# unbound server certificate file.
	server-cert-file: "/etc/unbound/unbound_server.pem"

	# unbound-control key file.
	control-key-file: "/etc/unbound/unbound_control.key"

	# unbound-control certificate file.
	control-cert-file: "/etc/unbound/unbound_control.pem"

# Stub and Forward zones
include: /etc/unbound/conf.d/*.conf

# Stub zones.
# Create entries like below, to make all queries for 'example.com' and
# 'example.org' go to the given list of nameservers. list zero or more
# nameservers by hostname or by ipaddress. If you set stub-prime to yes,
# the list is treated as priming hints (default is no).
# With stub-first yes, it attempts without the stub if it fails.
# Consider adding domain-insecure: name and local-zone: name nodefault
# to the server: section if the stub is a locally served zone.
# stub-zone:
#	name: "example.com"
#	stub-addr: 192.0.2.68
#	stub-prime: no
#	stub-first: no
#	stub-ssl-upstream: no
# stub-zone:
#	name: "example.org"
#	stub-host: ns.example.com.

# You can now also dynamically create and delete stub-zone's using
# unbound-control stub_add domain.com 1.2.3.4 5.6.7.8
# unbound-control stub_remove domain.com 1.2.3.4 5.6.7.8

# Forward zones
# Create entries like below, to make all queries for 'example.com' and
# 'example.org' go to the given list of servers. These servers have to handle
# recursion to other nameservers. List zero or more nameservers by hostname
# or by ipaddress. Use an entry with name "." to forward all queries.
# If you enable forward-first, it attempts without the forward if it fails.
# forward-zone:
# 	name: "example.com"
# 	forward-addr: 192.0.2.68
# 	forward-addr: 192.0.2.73@5355  # forward to port 5355.
# 	forward-first: no
# 	forward-ssl-upstream: no
# forward-zone:
# 	name: "example.org"
# 	forward-host: fwd.example.com
#
# You can now also dynamically create and delete forward-zone's using
# unbound-control forward_add domain.com 1.2.3.4 5.6.7.8
# unbound-control forward_remove domain.com 1.2.3.4 5.6.7.8

# Views
# Create named views. Name must be unique. Map views to requests using
# the access-control-view option. Views can contain zero or more local-zone
# and local-data options. Options from matching views will override global
# options. Global options will be used if no matching view is found.
# With view-first yes, it will try to answer using the global local-zone and
# local-data elements if there is no view specific match.
# view:
#	name: "viewname"
#	local-zone: "example.com" redirect
#	local-data: "example.com A 192.0.2.3"
# 	local-data-ptr: "192.0.2.3 www.example.com"
#	view-first: no
# view:
#	name: "anotherview"
#	local-zone: "example.com" refuse

"""
    Sour_unbound_area_config = '''
# You can add locally served data with
	local-zone: "local." static
	local-data: "mycomputer.local. IN A 192.0.2.51"
    local-data-ptr: "192.0.2.3 www.example.com"

# You can redirect a domain to a fixed address with
	# (this makes example.com, www.example.com, etc, all go to 192.0.2.3)
	# local-zone: "example.com" redirect
	# local-data: "example.com A 192.0.2.3"
	#
	# Shorthand to make PTR records, "IPv4 name" or "IPv6 name".
	# You can also add PTR records using local-data directly, but then
	# you need to do the reverse notation yourself.
'''
    try:
        with open("/etc/unbound/area.inorptrlist","w+") as f:
            f.write(Sour_unbound_area_config)
        os.system(edit + "/etc/unbound/area.inorptrlist")
        with open("/etc/unbound/area.inorptrlist","r") as f:
            unbound_area_config = f.read()
        with open("/etc/unbound/unbound.conf", "w+") as f:
            f.write(unbound_config + unbound_area_config)
    except:
        null = ""







#=============================================================#
if Sys_Init_Status == 1:
    Sys_Init(Sys_Init_Options[0], Sys_Init_Options[1], Sys_Init_Options[2], Sys_Init_Options[3], Sys_Init_Options[4], Sys_Init_Options[5])
#-------------------------------------
if Services_List[0] == 1:
    samba_configure()
if Services_List[1] == 1:
    postfix_configure(Postfix_Options[0], Postfix_Options[1], Postfix_Options[2], Postfix_Options[3], Postfix_Options[4])
if Services_List[2] == 1:
    nfs_configure()
if Services_List[3] == 1:
    nis_configure(Nis_Options[0])
if Services_List[4] == 1:
    ftp_configure(Ftp_Options[0], Ftp_Options[1], Ftp_Options[2], Ftp_Options[3], Ftp_Options[4])
#-------------------------------------
if Services_List0[0] == 1:
    apache_configure(Apache_Options[0], Apache_Options[1], Apache_Options[2])
if Services_List0[1] == 1:
    bind_configure(Bind_Options[0], Bind_Options[1], Bind_Options[2])
if Services_List0[2] == 1:
    Unbound_configure()
if Services_List0[3] == 1:
    PXE_Server(Pxe_Options[0], Pxe_Options[1], Pxe_Options[2], Pxe_Options[3], Pxe_Options[4], Pxe_Options[5], Pxe_Options[6], Pxe_Options[7], Pxe_Options[8], Pxe_Options[9], Pxe_Options[10], Pxe_Options[11])
if Services_List0[4] == 1:
    sendmail_configure(Sendmail_Options[0], Sendmail_Options[1])
#=============================================================#