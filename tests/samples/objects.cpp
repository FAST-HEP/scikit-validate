#include "TObject.h"
#include "TSystem.h"
#include "TTree.h"
#include "TFile.h"
#include "TVector2.h"
#include "TVector3.h"
#include <vector>


class A {
public:
        A() :
                start_ns(0),
                end_ns(0){

        };
        virtual ~A(){

        };
        float start_ns;
        float end_ns;
};

class B {
public:
        B() :
                driftTime(0),
                xyPosition(),
                xyzPosition() {

        };
        virtual ~B(){

        };
        float driftTime;
        TVector2 xyPosition;
        TVector3 xyzPosition;

};

class MyEvent: public TObject {
public:
        MyEvent() :
                eventID(0),
                ayes(),
                bees(){

        };
        virtual ~MyEvent(){

        };
        unsigned int eventID;
        std::vector<A> ayes;
        std::vector<B> bees;
        ClassDef(MyEvent, 2);
};

void objects(){
        TFile* file = new TFile("objects.root", "RECREATE");
        TTree* tree = new TTree("Events", "My Events");

        MyEvent *event = new MyEvent();
        tree->Branch("MyEvent", &event);



        for(Int_t ev = 0; ev < 1000; ++ev) {
                // cout << "event " << ev << endl;
                event->eventID = ev;

                std::vector<A> ayes;

                for(Int_t a=1; a < 3; ++a) {
                        A new_a = A();
                        new_a.start_ns = ev + 1*a;
                        new_a.end_ns = ev + 2*a;
                        ayes.push_back(new_a);
                }
                std::vector<B> bees;
                for(Int_t b=1; b < 3; ++b) {
                        B new_b = B();
                        new_b.driftTime = b*2 + 3;
                        new_b.xyPosition = TVector2(b, -b);
                        new_b.xyzPosition = TVector3(b, 2*b, -b);
                        bees.push_back(new_b);
                }
                event->ayes = ayes;
                event->bees = bees;
                tree->Fill();
                event->Clear();
        }
        tree->Write();
        tree->Print();
        delete file;
}
