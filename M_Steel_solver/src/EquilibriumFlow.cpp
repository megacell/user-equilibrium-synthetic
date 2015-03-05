/*
    Copyright 2008, 2009 Matthew Steel.

    This file is part of EF.

    EF is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    EF is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with EF.  If not, see <http://www.gnu.org/licenses/>.
*/


#include <utility> //For Pair
#include <iostream>
#include <fstream>
#include <cstdlib> //For EXIT_SUCCESS

#include "MTimer.hpp"
#include "AlgorithmBSolver.hpp"
#include "BarGeraImporter.hpp"
#include "InputGraph.hpp"

using namespace std;

void general(const char* netString, const char* tripString, double distanceFactor=0.0, double tollFactor=0.0, double gap = 1e-13)
{
	ifstream network(netString), trips(tripString);
	BarGeraImporter bgi(distanceFactor, tollFactor);
	InputGraph ig;
	MTimer timer3;
	bgi.readInGraph(ig, network, trips);
	cout << timer3.elapsed() << endl;

	MTimer timer1;

	AlgorithmBSolver abs(ig);
	double time=0.0;
	cout << (time += timer1.elapsed()) << endl;//*/
//*/
	double thisGap;
	for(thisGap = abs.averageExcessCost(); thisGap > gap; thisGap = abs.averageExcessCost()) {
		cout << time << ' ' << thisGap << endl;
		MTimer t2;
		//cout << i << endl;
		abs.solve(12);
		time += t2.elapsed();
	}
	cout << time << ' ' << thisGap << endl;
	cout << abs << endl;
        ////Output a file with all the flows
        ofstream myfile;
        myfile.open ("output.txt");
        myfile << abs;
        myfile.close();
//*/
}

class func {
	public:
		func(double first, double second) : first(first), second(second) {}
		double operator()(double d) { return d*second + first; }
	private:
		double first, second;
};

int main (int argc, char **argv)
{
        cout << "Starting to load the network";
//	general("networks/ChicagoSketch/ChicagoSketch_net.txt", "networks/ChicagoSketch/ChicagoSketch_trips.txt", 0.04, 0.02);
//     	general("networks/ChicagoRegional/ChicagoRegional_net.txt", "networks/ChicagoRegional/ChicagoRegional_trips.txt", 0.25, 0.1, 1e-5);
//	general("networks/Braess/Braess_net.txt", "networks/Braess/Braess_trips.txt");
//      general("networks/TestExample/TestExample_net.txt", "networks/TestExample/TestExample_trips.txt");
        general("networks/OSM_medium/OSM_medium_net.txt", "networks/OSM_medium/OSM_medium_trips.txt");
//	general("networks/Auckland_net2.txt", "networks/Auckland_trips.txt");
//	general("networks/SiouxFalls_net.txt", "networks/SiouxFalls_trips.txt");
//	general("networks/Anaheim_net.txt", "networks/Anaheim_trips.txt");
//	general("networks/Philadelphia_network.txt", "networks/Philadelphia_trips.txt", 0.0, 0.055, 1e-4);

	 //Braess' network paradox
/*	InputGraph g;
	g.setNodes(5);
	g.addEdge(0, 1, func(0.5,0));
	g.addEdge(0, 4, func(0.5,0));
	g.addEdge(0, 2, func(1.5,0));
	g.addEdge(0, 3, func(2.5,0));
	g.addEdge(1, 4, func(0.5,3));
	g.addEdge(2, 4, func(0.5,1));
	g.addEdge(3, 4, func(0.5,2));
	
	g.addDemand(0, 4, 20.0);
	AlgorithmBSolver abs(g);
	cout << abs << endl;
	abs.solve(1);
	cout << abs << endl;
	//*/
}