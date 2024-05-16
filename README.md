# GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24
The working repository for my OMSCY Practicum Summer semester 2024 (13 May - 25 July).

### Initial Idea:
The problem I would like to try to solve will be implementing zero trust for (a) bus architecture. This is probably a mixture of CS/ECE problem. This is something I've given a lot of thought to but have never had the chance to work on. Bus architectures (e.g. CAN bus, Modbus, MIL-STD-1553, ARINC429, etc) are used in Cyber Physical Systems every day, ranging from critical infrastructure/ICS, the defense industrial base, to airplanes and the cars we all drive. The White House has put forth direction for US Gov agencies and recommendations for businesses to transition to zero trust. The problem is that many older technologies run on a mix of traditional IT with operational technology (OT). The latter usually involves some sort of bus system, which is inherently designed as 100% trust. If someone were to get on the bus, they could inherently send commands to any other device listening, most of the time those devices being actuators or controllers that can cause real world damage. Because of time limitations, I will probably have to choose a single bus architecture/standard to defend. My ideas for a solution are:

- Some digital twin/virt monitoring software
- bus IDS device with similar ethos/functionality to Snort
- Machine Learning AI -in-the-loop IPS that learns normal traffic and catches & stops malicious (but still bus compliant) commands.

### Research
- https://forums.ni.com/t5/Example-Code/Arinc-429-Rx-Implementation-in-LabVIEW-FPGA/ta-p/3507624
- https://github.com/aeroneous/PyARINC429
- https://www.computer.org/csdl/magazine/ic/2023/05/10217033/1PBNDAyn5YY
- https://www.swri.org/podcast/ep64
- https://www.swri.org/automotive-cyber-security
- https://abaco.com/blog/why-you-need-secure-your-1553-mil-std-bus-and-five-things-you-must-have-your-solution
- https://abaco.com/blog/what-zero-trust-and-why-you-should-implement-it
- https://www.altadt.com/mil-std-1553-cybersecurity-design-and-test-methodologies/
- https://sitaltech.com/
- https://en.wikipedia.org/wiki/ARINC_429
- https://arincinstruments.com/knowledge-base-2/ground-equipment-knowledge-base/getting-started/ai429-usb-model-ethernet-setup/
- https://www.aim-online.com/wp-content/uploads/2019/07/aim-tutorial-oview429-190712-u.pdf
- https://kimdu.com/arinc-429-tutorial-a-step-by-step-guide/
- https://sitaltech.com/wp-content/uploads/2022/02/Arinc429_IPcore_V2.1.pdf
- https://www.aim-online.com/products-overview/tutorials/arinc-429-tutorial/
- https://www.ueidaq.com/arinc-429-tutorial-reference-guide
- https://en.wikipedia.org/wiki/MIL-STD-1553
- https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf
- https://rbei-etas.github.io/busmaster/
- https://whitehouse.gov/wp-content/uploads/2022/01/M-22-09.pdf
- https://aviation.stackexchange.com/questions/40900/why-use-different-data-bus-for-civil-and-military-avionics
- https://aviation-ia.sae-itc.com/standards/arinc429p1-19-dl-429p1-19-data-labels
- https://www.astronics.com/avionics-databus-tutorials
- https://naa.aero/
- https://en.wikipedia.org/wiki/List_of_most-produced_aircraft
- https://en.wikipedia.org/wiki/Cirrus_SR22
- https://cirrusaircraft.com/wp-content/uploads/2021/11/2022-SR22T-International-v4.pdf
