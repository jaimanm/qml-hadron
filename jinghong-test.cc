/*
**    Let's first try doing hadronization but turn off decay
*/

#include "Pythia8/Pythia.h"
#include <iostream>
#include <string>
#include <fstream>

using namespace Pythia8;

int main() {
  Pythia pythia;
  pythia.readString("ProcessLevel:all = off");
  pythia.readString("HadronLevel:Decay = off");

  // Restrict to u/d mesons
  pythia.readString("StringFlav:probStoUD = 0.0");
  pythia.readString("StringFlav:probQQtoQ = 0.0");
  pythia.readString("StringFlav:probSQtoQQ = 0.0");
  pythia.readString("StringFlav:probQQ1toQQ0 = 0.0");
  pythia.readString("StringFlav:mesonUDvector = 0.0");
  pythia.readString("StringFlav:etaSup = 0.0");
  pythia.readString("StringFlav:etaPrimeSup = 0.0");


  pythia.init();
  Event& event = pythia.event;
  int nEvent = 10000;  // Number of events to generate
  double energy = 50.0;

  std::ofstream ofs("first_emission_" + std::to_string(static_cast<int>(energy)) + "gev.csv");
  ofs << "Event,Name,Pid,Particle_px,Particle_py,Particle_pz,Particle_E,Particle_pT\n";

  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    event.reset();

    // Add quark-antiquark string (example momenta)
    event.append(1, 23, 101, 0, 0.0, 0.0, energy, energy, 0.0);  // d quark
    event.append(-1, 23, 0, 101, 0.0, 0.0, -energy, energy, 0.0);  // anti-d quark

    if (!pythia.next()) {
      cout << "Hadronization failed!" << endl;
      continue;
    }

    // Output first emission
    for(const Particle& p: event){
      if(p.isFinal()){
        ofs << iEvent << ","
            << p.name() << ","
            << p.id() << ","
            << p.px() << ","
            << p.py() << ","
            << p.pz() << ","
            << p.e()  << ","
            << p.pT() << "\n";
        break; // only output first hadron
      }
    }
    
  }

  ofs.close();

  pythia.stat();  // Optional: Print statistics
  return 0;
}
