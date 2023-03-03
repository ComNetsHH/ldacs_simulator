import inet.node.inet.ManetRouter;
import inet.common.scenario.ScenarioManager;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;

network mobility
{
    parameters:
        int numAircraftsGroup1 = default(15);
        int numAircraftsGroup2 = default(15);
        string mobility_file_1 = "mobility_data/mobility_group1.txt";
        string mobility_file_2 = "mobility_data/mobility_group2.txt";
        string scenarioManager_file_1 = "mobility_data/scenario_group.xml";
        // string scenarioManager_file_2 = "mobility_data/scenario_group2.xml";
        @display("bgb=10000000,10000000;bgl=2");
        @figure[title](type=label; pos=0,-1; anchor=sw; color=darkblue);
    submodules:
        scenarioManager: ScenarioManager;
        radioMedium: <default("UnitDiskRadioMedium")> like IRadioMedium {
            @display("p=580,275");
        }
        configurator: Ipv4NetworkConfigurator {
            parameters:
                @display("p=100,100;is=s");
        }
        
        aircraft_group1[numAircraftsGroup1]: ManetRouter {
            @display("i=aircraft");
        }
        aircraft_group2[numAircraftsGroup2]: ManetRouter {
            @display("i=aircraft");
        }
}
