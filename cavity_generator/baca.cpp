#include<sstream>
#include<fstream>
#include<iostream>
#include<vector>
#include<string>
int main()
{
    int n_awal = 0;
    for(int i=0; i<1; i++)
    {
        int cav_count = 1321;
        std::stringstream namafile;
        namafile << "vertex" << i << ".py";
        std::ofstream fout(namafile.str());
        if (!fout.is_open())
        {
            std::cerr << "File output tidak dapat dibuka" << std::endl;
            return 1;
        }
        for (int n=n_awal; n<cav_count+n_awal; n++)
        {
            std::stringstream nama;
            nama << "data/Output_" << n << ".csv";
            std::ifstream baca(nama.str());
            //seandainya file nggak bisa dibuka
            if (!baca.is_open())
            {
                std::cerr << "Tidak dapat membuka file" << std::endl;
                return 1; //ouh ini dari int main ya
            }
            //simpan data csv di sini
            std::vector<std::vector<double>> data;
            std::string line;
            while (std::getline(baca, line)) //ini baca row nya
            {
                std::vector<double> row;
                std::stringstream ss(line);
                std::string value;
                while(std::getline(ss,value,','))
                {
                    row.push_back(std::stod(value));
                }
                data.push_back(row);
            }
            baca.close();
            fout << "vertices" << n-n_awal << " = [ \n";
            for (int i=0; i<data.size(); i++)
            {
                if (i == data.size()-1) //berarti baris yang terakhir
                {
                    fout << "{\"X\" : \" " << data[i][1]<< "cm\", ";
                    fout << "\"Y\" : \" " << data[i][2]<< "cm\", ";
                    fout << "\"Z\" : \" " << 0 << "cm\"";
                    fout << "},\n";
                }
                else
                {
                    fout << "{\"X\" : \" " << data[i][1]<< "cm\", ";
                    fout << "\"Y\" : \" " << data[i][2]<< "cm\", ";
                    fout << "\"Z\" : \" " << 0 << "cm\"";
                    fout << "},\n";
                }       
            }
            fout << "] \n";
        }
        fout << "vertices = [";
        for (int i=0; i<cav_count; i++)
        {
            if (i==cav_count-1)
            {
                fout << "vertices" << i << "]";
            }
            else
            {
                fout << "vertices" << i << ", \n \t \t \t";
            }
        }
        fout.close();
        n_awal += cav_count;
    }
    return 0;
}
