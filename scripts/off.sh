gpio1=67
state='in'
 
if [ ! -d /sys/class/gpio/$gpio1 ]; then echo $gpio1 > /sys/class/gpio/export; fi
click() {
    #state="`cat /sys/class/gpio/gpio$1/direction`"
    echo $state > /sys/class/gpio/gpio$1/direction
}
 
click $gpio1
