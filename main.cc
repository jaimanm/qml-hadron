#include "Pythia8/Pythia.h"  // Include Pythia8 main header for Monte Carlo event generation
#include <iostream>           // Standard I/O for console output
#include <fstream>            // File I/O for saving momentum data
using namespace Pythia8;      // Use Pythia8 namespace to avoid prefixing all classes

int main() {
  // Create main Pythia instance - the central object that controls all event generation
  Pythia pythia;

  // Disable all hard process generation - we will manually set up initial state particles
  // ProcessLevel:all = off means no QCD/QED processes will be automatically generated
  pythia.readString("ProcessLevel:all = off");

  // Initialize Pythia with current settings - loads particle data, PDFs, and prepares for generation
  pythia.init();

  // Get reference to the event record - this is where all particles in the current event are stored
  Event& event = pythia.event;

  int nEvent = 10;  // Number of events to generate
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    // Clear the event record from previous event - prepares for new event generation
    event.reset();

    // Manually add a down quark to the event record
    // Parameters: id, status, mother1, mother2, px, py, pz, E, mass
    // id=1 (down quark), status=23 (incoming parton for hadronization)
    // Colors: 101 (color index), 0 (anticolor index) - forms color singlet with antiquark
    // Momentum: (0,0,5,5,0) GeV - along +z direction
    event.append(1, 23, 101, 0, 0.0, 0.0, 5.0, 5.0, 0.0);  // d quark

    // Manually add an anti-down quark to the event record
    // id=-1 (anti-down quark), status=23 (incoming parton for hadronization)
    // Colors: 0 (color), 101 (anticolor) - pairs with above quark to form color singlet
    // Momentum: (0,0,-5,5,0) GeV - along -z direction, opposite to quark
    event.append(-1, 23, 0, 101, 0.0, 0.0, -5.0, 5.0, 0.0);  // anti-d quark

    // Generate the next event - performs hadronization of the quark-antiquark string
    // pythia.next() handles: parton showers, hadronization, decays, and beam remnants
    // Returns false if event generation fails (rare, usually due to numerical issues)
    if (!pythia.next()) {
      std::cout << "Hadronization failed!" << std::endl;
      continue;  // Skip to next event if hadronization fails
    }

    // Output final-state hadrons from this event
    std::cout << "Event " << iEvent << ":" << std::endl;
    for (int i = 0; i < event.size(); ++i) {  // Loop through all particles in event
      // Check if particle is final-state (not decayed) AND is a hadron (not lepton/photon/etc.)
      if (event[i].isFinal() && event[i].isHadron()) {
        // Print hadron name and PDG ID (Particle Data Group identification number)
        std::cout << "  " << event[i].name() << " (ID: " << event[i].id() << ")" << std::endl;
      }
    }
  }

  // Save momentum data to file for analysis
  std::ofstream momentumFile("momentum_data.csv");
  momentumFile << "# Event,Particle_ID,px,py,pz,E,mass" << std::endl;

  // Re-run events to collect momentum data
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    event.reset();

    // Add quark-antiquark string (example momenta)
    event.append(1, 23, 101, 0, 0.0, 0.0, 5.0, 5.0, 0.0);  // d quark
    event.append(-1, 23, 0, 101, 0.0, 0.0, -5.0, 5.0, 0.0);  // anti-d quark

    if (!pythia.next()) {
      std::cout << "Hadronization failed!" << std::endl;
      continue;
    }

    // Save momentum data for final-state hadrons
    for (int i = 0; i < event.size(); ++i) {
      if (event[i].isFinal() && event[i].isHadron()) {
        momentumFile << iEvent << ","
                     << event[i].id() << ","
                     << event[i].px() << ","
                     << event[i].py() << ","
                     << event[i].pz() << ","
                     << event[i].e() << ","
                     << event[i].m() << std::endl;
      }
    }
  }

  momentumFile.close();

  // Print final statistics - shows cross sections, efficiencies, and generation summary
  pythia.stat();

  return 0;
}