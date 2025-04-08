#include<iostream>
#include<fstream>
#include"latin.h"
#include<vector>
#include<sstream> 
#include<iomanip>

//pertama, kita definisikan objek titik 2D
struct Point
{
    double x, y;
};

double basisFunction(int i, int p, double u, const std::vector<double> &knots)
{
    //i itu yang diiterasikan, p orde basisnya, u parameternya, knots itu vektor knotnya
    if(p==0) //orde ke nol
    {
        
        if (knots[i]<=u && u < knots[i+1])
        {
            return 1.0;
        }
        else
        {
            return 0.0;
        }
        
        //return (knots[i]<=u && u<knots[i+1])? 1.0:0.0;
    }
    else
    {
        double left = (u-knots[i])/(knots[i+p]-knots[i])*basisFunction(i,p-1,u,knots);
        double right = (knots[i+p+1]-u)/(knots[i+p+1]-knots[i+1])*basisFunction(i+1,p-1,u,knots);
        
        if(std::isnan(left))
        {
            left = 0.0;
        }
        if(std::isnan(right))
        {
            right = 0.0;
        }
        return left+right;
        //return (std::isnan(left)? 0.0 : left) + (std::isnan(right)? 0.0 : right);
    }
}


//evaluasi titik nurbs, pakai sumasi
Point evaluateNURBS(double u, int degree, const std::vector<Point> &controlPoints, const std::vector<double> &weights, const std::vector<double>&knots)
{
    //jadi ini posisi x dan y saling independen, artinya kita bisa kerjakan secara terpisah
    double sumX = 0.0;
    double sumY = 0.0;
    double sumDenominator = 0.0;

    for (int i=0; i<controlPoints.size(); i++)
    {
        double weightN_ip = basisFunction(i, degree, u, knots)*weights[i];
        sumX += weightN_ip*controlPoints[i].x;
        sumY += weightN_ip*controlPoints[i].y;
        sumDenominator += weightN_ip;
    }
    Point result;
    result.x = sumX/sumDenominator;
    result.y = sumY/sumDenominator;
    return result;
}

void outFile(const std::vector<Point> &vertex, int n)
{
    std::stringstream nama;
    nama << "data/Output_" << n << ".csv";
    std::ofstream fout(nama.str());
    fout << std::fixed << std::setprecision(7);
    for (int i=0; i<vertex.size(); i++)
    {
        fout << i << "," << vertex[i].x << "," << vertex[i].y << "\n";
    }
    fout.close();
}
void outPlot(const std::vector<Point> &vertex, int n)
{
    std::stringstream nama;
    nama << "for_plot/Output_" << n << ".csv";
    std::ofstream fout(nama.str());
    fout << std::fixed << std::setprecision(7);
    for (int i=0; i<vertex.size(); i++)
    {
        fout << i << "," << vertex[i].x << "," << vertex[i].y << "\n";
    }
    fout.close();
}
void outControlPoints(std::vector<Point> &control, int n)
{
    std::stringstream nama;
    nama << "control_point/control_" << n << ".csv";
    std::ofstream fout(nama.str());
    fout << std::fixed << std::setprecision(7);
    for (int i=0; i<control.size(); i++)
    {
        fout << control[i].x << "," << control[i].y << "\n";
    }
    fout.close();
}

std::vector<Point> mirrory(const std::vector<Point> &vertex) //dari atas pantul ke bawah
{
    std::vector<Point> mirry = vertex;
    std::vector<Point> mirrx;
    for (int i=vertex.size()-1; i>=0; i--)
    {
        Point mirror = {vertex[i].x, -vertex[i].y};
        mirry.emplace_back(mirror);
    }
    //pantulkan dari kanan ke kiri
    for (int i=0; i<mirry.size(); i++)
    {
        mirrx.emplace_back(mirry[i]); //nggak bisa diinisiasi pakai mirr = vertex kayaknya di atas
    }
    for (int i=mirry.size()-1; i>=0; i--)
    {
        Point mirror = {-mirry[i].x, mirry[i].y};
        mirrx.emplace_back(mirror);
    }
    return mirrx;
}

std::vector<Point> removeDuplicates(const std::vector<Point>& points) {
    std::vector<Point> uniquePoints;
    for (const auto& pt : points) 
    { //empty itu untuk awalan. kemudian dilakukan perbandingan dengan titik sebelumnya
        if (uniquePoints.empty() || !(std::abs(pt.x - uniquePoints.back().x) < 1e-9 && std::abs(pt.y - uniquePoints.back().y) < 1e-9)) 
        {
            uniquePoints.push_back(pt);
        }
    }
    return uniquePoints;
}



int main()
{
    int jumlah_sampel = 500; //untuk baca data, ini sekedar placeholder (sementara ini)
    std::vector<double> knots = {0.0,1.0,1.0,2.0,2.0,3.0,4.0,4.0,5.0,5.0,6.0};
    int degree = 4;
    //int sampel = 20;
    std::ofstream paramout("input_parameter.csv");
    paramout << std::fixed << std::setprecision(9);
    dataset latinh(jumlah_sampel); //inisiasi ulang untuk setiap bentuk cavity
    std::vector<std::vector<double>> pareto = latinh.bacaData("renormalized_input_separated_pareto.csv"); //format nya renormalized_input_i
    //std::ofstream fout("belum_diacak.csv");
    //std::ofstream gout("sudah_diacak.csv");
    int sampel_baca = pareto.size(); 
    for(int i=0; i<sampel_baca; i++)
    {
        std::vector<Point> vertex;
        //parameter yang nilainya fix (ditaruh di dalam, biar nggak bikin bingung, nggak terlalu nambah overhead juga)
        double x0 = 0; 
        double y0 = pareto[i][0]; 
        double xinter = pareto[i][1]; //x1
        double yinter = y0; //y1
        double x1 = xinter; //x2
        double y1 = pareto[i][2]; //y2
        double x4 = pareto[i][3]; //x3
        double y4 = pareto[i][4]; //y3
        double x5 = x4; //x4
        double y5 = pareto[i][5]; //y4
        double x6 = 25; //x5
        double y6 = y5; //y5
        double x7 = 25; //x6
        double y7 = 0; //y6
        //selanjutnya variasi bobot
        double w0 = pareto[i][6];
        double winter = pareto[i][7];
        double w1 = pareto[i][8];
        double w4 = pareto[i][9];
        double w5 = 5;
        double w6 = 10; 
        //output parameter untuk training neural network (ada 10 parameter)
        paramout << y0 << "," << xinter << "," << y1 <<  "," << x4 << "," << y4 << ",";
        paramout << y5 << "," << w0 << "," << winter << "," << w1 << "," << w4 << "\n";
        std::vector<Point> controlPoints = {{x0,y0},{xinter,yinter},{x1,y1},{x4,y4},{x5,y5},{x6,y6}};
        std::vector<double> weights = {w0,winter,w1,w4,w5,w6};
        Point pt0 = {x0,y0};
        for(double u=0.06; u<=6.0; u+=0.09)
        {
            Point pt = evaluateNURBS(u, degree, controlPoints, weights, knots);
            vertex.emplace_back(pt);
        }
        vertex = removeDuplicates(vertex);
        std::vector<Point> mirroredy;
        mirroredy = mirrory(vertex);
        Point ujung = {25,0};
        vertex.emplace_back(ujung);
        outPlot(vertex,i);
        mirroredy.emplace_back(pt0); //harus ditutup
        outFile(mirroredy,i);
        outControlPoints(controlPoints, i);
    }
    paramout.close();
}