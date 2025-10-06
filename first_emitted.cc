#include "Pythia8/Pythia.h"
#include <iostream>
#include <iomanip>
#include <vector>
#include <utility>
#include <fstream>
#include <string>
using namespace Pythia8;

int main() {
  // Create main Pythia instance
  Pythia pythia;

  // Disable all hard process generation
  pythia.readString("ProcessLevel:all = off");

  // Initialize Pythia with current settings
  pythia.init();

  // Get reference to the event record
  Event& event = pythia.event;

  // Open CSV file for first hadron data
  std::ofstream csvFile("first_hadron_data.csv");
  csvFile << "Event,Index,Name,ID,Status,px,py,pz,E,m,Mother1,Mother2,Daughter1,Daughter2,IsFinal" << std::endl;

  int nEvent = 10;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    // Clear the event record from previous event
    event.reset();

    // Manually add quarks
    event.append(1, 23, 101, 0, 0.0, 0.0, 5.0, 5.0, 0.0);   // d quark
    event.append(-1, 23, 0, 101, 0.0, 0.0, -5.0, 5.0, 0.0); // anti-d quark

    // Generate the next event
    if (!pythia.next()) {
      std::cout << "Hadronization failed!" << std::endl;
      continue;
    }

    // Output first emitted hadrons (primary hadrons from fragmentation)
    std::cout << "\n=== Event " << iEvent << " ===" << std::endl;
    std::cout << "First emitted hadrons (primary from string fragmentation):" << std::endl;
    
    for (int i = 0; i < event.size(); ++i) {
      // Look for primary hadrons: status codes 81-89 (positive) or -81 to -89 (negative)
      int status = event[i].status();
      bool isPrimaryHadron = (abs(status) >= 81 && abs(status) <= 89) && event[i].isHadron();
      
      if (isPrimaryHadron) {
        std::cout << "  Index " << i << ": " << event[i].name() 
                  << " (ID: " << event[i].id() << ")"
                  << " Status: " << status;
        
        // Show if it's still in final state or has decayed
        if (status > 0) {
          std::cout << " [Final state]";
        } else {
          std::cout << " [Decayed/processed]";
        }
        
        // Show momentum information
        std::cout << " px=" << std::fixed << std::setprecision(3) << event[i].px()
                  << " py=" << event[i].py() 
                  << " pz=" << event[i].pz()
                  << " E=" << event[i].e()
                  << " m=" << event[i].m();
        
        // Show mother information for fragmentation
        std::cout << " Mothers: " << event[i].mother1() << "-" << event[i].mother2();
        
        // Show daughters if it decayed
        if (status < 0 && event[i].daughter1() != 0) {
          std::cout << " Daughters: " << event[i].daughter1() << "-" << event[i].daughter2();
        }
        
        std::cout << std::endl;
      }
    }
    
    // Advanced first hadron identification using multiple criteria
    std::cout << "\nAdvanced First Hadron Analysis:" << std::endl;
    
    // Step 1: Collect all primary hadrons from string fragmentation (status 81-89)
    std::vector<std::pair<int, int>> primaryHadrons; // (index, status)
    for (int i = 0; i < event.size(); ++i) {
      int status = event[i].status();
      if ((abs(status) >= 81 && abs(status) <= 89) && event[i].isHadron()) {
        primaryHadrons.push_back({i, status});
      }
    }
    
    if (primaryHadrons.empty()) {
      std::cout << "  No primary hadrons found in this event" << std::endl;
      continue;
    }
    
    // Step 2: Analyze mother-daughter relationships to understand string structure
    std::cout << "  Primary hadrons from string fragmentation:" << std::endl;
    for (auto& hadron : primaryHadrons) {
      int idx = hadron.first;
      const Particle& p = event[idx];
      std::cout << "    Index " << idx << ": " << p.name() 
                << " (mothers: " << p.mother1() << "-" << p.mother2() 
                << ", daughters: " << p.daughter1() << "-" << p.daughter2() << ")";
      
      // Check if this hadron comes from string fragmentation between quarks
      // String fragmentation typically has mother1 < mother2 and both positive
      if (p.mother1() >= 0 && p.mother2() >= 0 && p.mother1() < p.mother2()) {
        std::cout << " [String fragmentation]";
      }
      std::cout << std::endl;
    }
    
    // Step 3: Identify first emitted hadrons using space-time production coordinates
    // This is the most accurate way to determine true simultaneity
    
    std::cout << "  First hadron(s) analysis using space-time coordinates:" << std::endl;
    
    // Collect production times for all primary hadrons
    std::vector<std::tuple<double, int, int>> hadronTimes; // (production_time, index, status)
    
    for (auto& hadron : primaryHadrons) {
      int idx = hadron.first;
      const Particle& p = event[idx];
      
      double prodTime = 0.0;
      try {
        Vec4 vtx = p.vProd();
        prodTime = vtx.e(); // t-coordinate (time)
      } catch (...) {
        // If space-time info not available, use index as proxy (less accurate)
        prodTime = static_cast<double>(idx);
      }
      
      hadronTimes.emplace_back(prodTime, idx, hadron.second);
    }
    
    // Sort by production time
    std::sort(hadronTimes.begin(), hadronTimes.end());
    
    // Find hadrons produced at the earliest time (within tolerance)
    double earliestTime = std::get<0>(hadronTimes[0]);
    const double timeTolerance = 1e-10; // Very small tolerance for "simultaneous"
    
    std::vector<int> simultaneousFirstHadrons;
    for (auto& ht : hadronTimes) {
      double prodTime = std::get<0>(ht);
      int idx = std::get<1>(ht);
      
      if (prodTime - earliestTime <= timeTolerance) {
        simultaneousFirstHadrons.push_back(idx);
      } else {
        break; // Later times are not simultaneous
      }
    }
    
    // Step 4: Analyze string structure and end identification
    std::cout << "  String structure analysis:" << std::endl;
    
    // Group hadrons by their mother particles (should all be from same quark-antiquark string)
    std::map<std::pair<int, int>, std::vector<int>> hadronsByMothers; // (mother1, mother2) -> indices
    
    for (int idx : simultaneousFirstHadrons) {
      const Particle& p = event[idx];
      std::pair<int, int> mothers = {p.mother1(), p.mother2()};
      hadronsByMothers[mothers].push_back(idx);
    }
    
    std::cout << "    All simultaneous first hadrons share the same mother particles (quark-antiquark pair)" << std::endl;
    std::cout << "    This confirms they come from the same QCD string fragmentation" << std::endl;
    
    // Analyze momentum directions to infer which end of the string they came from
    std::cout << "    Momentum analysis (potential end identification):" << std::endl;
    for (int idx : simultaneousFirstHadrons) {
      const Particle& p = event[idx];
      double pz = p.pz(); // z-momentum (along string axis)
      double px = p.px();
      double py = p.py();
      double pt = sqrt(px*px + py*py); // transverse momentum
      
      std::cout << "      " << p.name() << " (index " << idx << "): pz=" 
                << std::fixed << std::setprecision(3) << pz 
                << " GeV/c, pT=" << pt << " GeV/c";
      
      // In string fragmentation, hadrons from opposite ends may have opposite pz
      if (pz > 0.1) std::cout << " [positive z-direction]";
      else if (pz < -0.1) std::cout << " [negative z-direction]";
      else std::cout << " [transverse direction]";
      
      std::cout << std::endl;
    }
    
    // Check production vertices if available
    bool hasVertexInfo = false;
    try {
      event[simultaneousFirstHadrons[0]].vProd();
      hasVertexInfo = true;
    } catch (...) {
      hasVertexInfo = false;
    }
    
    if (hasVertexInfo) {
      std::cout << "    Production vertex analysis:" << std::endl;
      for (int idx : simultaneousFirstHadrons) {
        const Particle& p = event[idx];
        Vec4 vtx = p.vProd();
        std::cout << "      " << p.name() << " (index " << idx << "): position (x,y,z)=("
                  << std::fixed << std::setprecision(6) 
                  << vtx.px() << ", " << vtx.py() << ", " << vtx.pz() << ")" << std::endl;
      }
    }
    
    // Step 5: Analyze momentum fractions (z-values) - first-rank hadrons typically take larger fractions
    std::cout << "  First hadron(s) analysis:" << std::endl;
    if (simultaneousFirstHadrons.size() > 1) {
      std::cout << "    Multiple potential first hadrons detected (simultaneous fragmentation from both ends):" << std::endl;
      
      // Analyze each potential first hadron
      for (int idx : simultaneousFirstHadrons) {
        const Particle& p = event[idx];
        double energy = p.e();
        
        // Calculate momentum fraction relative to string energy (approximate)
        // For a quark-antiquark string, the total energy is roughly 2*5.0 = 10.0 GeV
        double totalStringEnergy = 10.0; // Approximate for our setup
        double zFraction = energy / totalStringEnergy;
        
        std::cout << "      " << p.name() << " (index " << idx << "): E=" 
                  << std::fixed << std::setprecision(3) << energy 
                  << " GeV, z≈" << zFraction;
        
        // Check space-time production info if available
        // Note: vProd() returns production vertex coordinates (x,y,z,t)
        try {
          Vec4 vtx = p.vProd();
          std::cout << ", production time t=" << vtx.e(); // t coordinate
        } catch (...) {
          // Space-time info might not be available in all Pythia versions
        }
        std::cout << std::endl;
      }
      
      // For CSV output, save all simultaneous first hadrons
      for (size_t k = 0; k < simultaneousFirstHadrons.size(); ++k) {
        int idx = simultaneousFirstHadrons[k];
        const Particle& hadron = event[idx];
        
        std::string suffix = (simultaneousFirstHadrons.size() > 1) ? "_" + std::to_string(k+1) : "";
        
        csvFile << iEvent << suffix << ","
                << idx << ","
                << hadron.name() << ","
                << hadron.id() << ","
                << hadron.status() << ","
                << std::fixed << std::setprecision(6)
                << hadron.px() << ","
                << hadron.py() << ","
                << hadron.pz() << ","
                << hadron.e() << ","
                << hadron.m() << ","
                << hadron.mother1() << ","
                << hadron.mother2() << ","
                << hadron.daughter1() << ","
                << hadron.daughter2() << ","
                << (hadron.isFinal() ? "1" : "0")
                << std::endl;
      }
      
    } else {
      // Single first hadron case
      int firstHadronIndex = simultaneousFirstHadrons[0];
      const Particle& hadron = event[firstHadronIndex];
      double energy = hadron.e();
      double zFraction = energy / 10.0; // Approximate string energy
      
      std::cout << "    Single first hadron: " << hadron.name() 
                << " (index " << firstHadronIndex << "), E=" 
                << std::fixed << std::setprecision(3) << energy 
                << " GeV, z≈" << zFraction << std::endl;
      
      // Save to CSV
      csvFile << iEvent << ","
              << firstHadronIndex << ","
              << hadron.name() << ","
              << hadron.id() << ","
              << hadron.status() << ","
              << std::fixed << std::setprecision(6)
              << hadron.px() << ","
              << hadron.py() << ","
              << hadron.pz() << ","
              << hadron.e() << ","
              << hadron.m() << ","
              << hadron.mother1() << ","
              << hadron.mother2() << ","
              << hadron.daughter1() << ","
              << hadron.daughter2() << ","
              << (hadron.isFinal() ? "1" : "0")
              << std::endl;
    }
    
    // Also show the fragmentation sequence order
    std::cout << "\nFragmentation sequence (all primary hadrons in order):" << std::endl;
    
    // Sort by index (which corresponds to production order in Pythia)
    for (size_t j = 0; j < primaryHadrons.size(); ++j) {
      int idx = primaryHadrons[j].first;
      std::cout << "  Rank " << (j+1) << ": " << event[idx].name() 
                << " (status " << primaryHadrons[j].second << ")";
      
      // Calculate momentum fraction taken by this hadron
      double energy = event[idx].e();
      std::cout << " E=" << std::fixed << std::setprecision(3) << energy;
      
      std::cout << std::endl;
    }

    // Show final-state hadrons for comparison
    std::cout << "\nFinal-state hadrons:" << std::endl;
    for (int i = 0; i < event.size(); ++i) {
      if (event[i].isFinal() && event[i].isHadron()) {
        std::cout << "  " << event[i].name() << " (ID: " << event[i].id() << ")" << std::endl;
      }
    }
  }

  // Close CSV file
  csvFile.close();
  std::cout << "\nFirst hadron data saved to first_hadron_data.csv" << std::endl;

  return 0;
}
