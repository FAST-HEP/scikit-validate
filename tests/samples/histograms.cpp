#include "TObject.h"
#include "TSystem.h"
#include "TTree.h"
#include "TFile.h"
#include "TVector2.h"
#include "TVector3.h"
#include <vector>

void histograms()
{
    TFile *file = new TFile("histograms.root", "RECREATE");
    TH1 *h1 = new TH1I("h1", "h1 title", 100, 0.0, 4.0);
    TH2 *h2 = new TH2F("h2", "h2 title", 40, 0.0, 2.0, 30, -1.5, 3.5);
    TH3 *h3 = new TH3D("h3", "h3 title", 80, 0.0, 1.0, 100, -2.0, 2.0,
                       50, 0.0, 3.0);

    TF2 *xyg = new TF2("xyg", "xygaus", 0, 10, 0, 10);
    TF3 *xyzg = new TF3("xyzg", "xyzgaus", 0, 10, 0, 10, 0, 10);
    xyg->SetParameters(1, 5, 2, 5, 2);
    xyzg->SetParameters(1, 5, 2, 5, 2, 5, 2);

    h1->FillRandom("gaus", 10000);
    h2->FillRandom("xyg", 10000);
    h3->FillRandom("xyzg", 10000);

    
    h1->Write();
    h2->Write();
    h3->Write();
    file->Close();
    delete file, xyg, xyzg;
}
