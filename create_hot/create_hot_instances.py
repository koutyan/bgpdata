# Author: Takehiko Momma

import os
import sys

if len(sys.argv) < 1 and not os.path.isfile(sys.argv[1]):
    print("err: invalid command: python", sys.argv[0], "analyzed_file")
    sys.exit(1)

f = open(sys.argv[1],"r",encoding='utf-8')

DIR = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(DIR + "/network")
filename = DIR + "/hot-instances.yaml" 
g = open(filename,"w")
g.write("heat_template_version: pike\n")
g.write("\n")
g.write("resources:\n")


s = 0

for line in f:
    l = line[:-1].split(" ")
    if s == 0:
        AS = l[1]
        s = 1
    elif s == 1:
        s = 2
    elif s == 2:
        #if AS == "15169":
        #    s = 0
        #    continue
        g.write("  as{0}:\n".format(AS))
        #g.write("    type: OS::Heat::ResourceGroup\n")
        #g.write("    properties:\n")
        g.write("    type: OS::Nova::Server\n")
        g.write("    properties:\n")
        g.write("      name: asxxx\n".replace("xxx",str(AS)))
        g.write("      image: Ubuntu\n")
        g.write("      flavor: m1.small\n")
        g.write("      networks:\n")
        for file in files:
            if "-"+AS in file or AS+"-" in file:
                g.write("        - network: {0}\n".format(str(file)))
        g.write("      security_groups:\n")
        g.write("        - AllAllow\n")
        g.write("      key_name: default\n")
        g.write("\n")
        
        g.write("  cinder_volume:\n)
        g.write("    type: OS::Cinder::Volume\n)
        g.write("    properties:\n)
        g.write("      size: { get_param: volume_size }\n)
        g.write("      availability_zone: { get_param: availability_zone }\n)
        g.write("  volume_attachment:\n)
        g.write("    type: OS::Cinder::VolumeAttachment\n)
        g.write("    properties:\n)
        g.write("      volume_id: { get_resource: cinder_volume }\n)
        g.write("      instance_uuid: { get_resource: nova_instance }\n)
        g.write("      mountpoint: /dev/vda\n)
        s = 0
g.close()
f.close()

