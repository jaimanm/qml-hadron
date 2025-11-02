#include "Pythia8/Pythia.h"
#include <iostream>
#include <fstream>
#include <cmath>
using namespace Pythia8;

int main() {
  Pythia pythia;
  pythia.readString("ProcessLevel:all = off");
  pythia.readString("HadronLevel:all = on");
  pythia.readString("HadronLevel:Decay = off");
  pythia.init();
  Event& event = pythia.event;
 
  
  std::ofstream ofs("/home/arjsur/pythia_results/events_output_100gev.csv");
  ofs << "Event,Particle,Particle_pz,Particle_pT,Particle_px,Particle_py,Particle_E\n";

  int nEvent = 10000;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    event.reset();

    event.append(1, 71, 101, 0, 0.0, 0.0, 50.0, 50.0, 0.0);
    event.append(-1, 71, 0, 101, 0.0, 0.0, -50.0, 50.0, 0.0);

    if (!pythia.next()) {
      std::cout << "Hadronization failed!" << std::endl;
      continue;
    }

    int mostEnergeticPion = -1;
    double maxEnergy = 0.0;
    
    for (int i = 0; i < event.size(); ++i) {
      int pidAbs = std::abs(event[i].id());
      if (pidAbs == 111 || pidAbs == 211) {
        if (event[i].isFinal()) {
          double energy = event[i].e();
          if (energy > maxEnergy) {
            maxEnergy = energy;
            mostEnergeticPion = i;
          }
        }
      }
    }

    if (mostEnergeticPion >= 0) {
      ofs << iEvent << ","
          << "\"" << event[mostEnergeticPion].name() << "\","
          << std::abs(event[mostEnergeticPion].pz()) << ","
          << event[mostEnergeticPion].pT() << ","
          << event[mostEnergeticPion].px() << ","
          << event[mostEnergeticPion].py() << ","
          << event[mostEnergeticPion].e() << "\n";
    }
  }

  ofs.close();

  pythia.stat();

  return 0;
}
