#include "Pythia8/Pythia.h"
#include <iostream>
#include <fstream>
#include <cmath>
using namespace Pythia8;

int main() {
  Pythia pythia;
  pythia.readString("ProcessLevel:all = off");
  pythia.readString("PartonLevel:ISR = on");
  pythia.readString("PartonLevel:FSR = on");
  pythia.init();
  Event& event = pythia.event;
 
  
  std::ofstream ofs("/home/arjsur/pythia_results/events_output_50gev.csv");
  ofs << "Event,Particle,Particle_pz,Particle_pT,Particle_px, Particle_py\n";

  int nEvent = 10000;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    event.reset();

    event.append(1, 71, 101, 0, 0.0, 0.0, 50.0, 50.0, 0.0);
    event.append(-1, 71, 0, 101, 0.0, 0.0, -50.0, 50.0, 0.0);

    if (!pythia.next()) {
      std::cout << "Hadronization failed!" << std::endl;
      continue;
    }

    for (int i = 0; i < event.size(); ++i) {
      if (event[i].isFinal() && event[i].isHadron()) {
        ofs << iEvent << ","
            << "\"" << event[i].name() << "\","
            << (std::abs(event[i].pz())) << ","
            << event[i].pT() << ","
            << event[i].px() << ","
            << event[i].py() << "\n";
        break;
      }
    }
  }

  ofs.close();

  pythia.stat();

  return 0;
}
