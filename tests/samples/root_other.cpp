#include "TObject.h"
#include "TSystem.h"
#include "TTree.h"
#include "TFile.h"
#include "TProfile.h"
#include "TParameter.h"
#include <vector>

void root_other()
{
    TFile *file = new TFile("root_other.root", "RECREATE");
    auto hprof = new TProfile("hprof", "Profile of pz versus px", 100, -4, 4, 0, 20);
    auto param = new TParameter<int>("test", 42);
    
    hprof->Write();
    param->Write();    
    file->Close();
    delete file, hprof;
}
