#ifndef LATIN_H
#define LATIN_H

#include<iostream>
#include<fstream>
#include<cmath>
#include<random>
#include<algorithm>
#include<sstream>
#include<string>
//pengen coba tanpa pakai std::vector

//pertama, random number generator dulu
class Rnd
{
    public:
        Rnd() : mersenne_gen{std::random_device()()}, rnd_dist{0.0,1.0} {}
        double munculkan()
        {
            return rnd_dist(mersenne_gen);
        }
        template <typename Iterator>
        void shuffle(Iterator begin, Iterator end)
        {
            std::shuffle(begin, end, mersenne_gen); 
        }
    private:
        std::mt19937 mersenne_gen;
        std::uniform_real_distribution<double> rnd_dist;
};

//idealnya kita bikin library buat LHS yang bisa dimasukin parameter sebarang dimensi.
//tapi perlu mikir juga, jadi mungkin nggak dulu deh. Pertama kita bikin objek matriks 2D dulu

class Matriks
{
    public:
        Matriks(int nbaris, int nkolom) : baris{nbaris}, kolom{nkolom} 
        {
            data = new double*[baris];
            for (int i=0; i<nbaris; i++)
            {
                data[i] = new double[kolom];
            }
            clear();
        }
        ~Matriks()
        {
            if (data == nullptr) return;
            for (int i=0; i<baris; i++)
            {
                delete[] data[i];
            }
            delete[] data;
            data = nullptr;
        }
        //ini kan datanya ditaruh di private, berarti kita butuh akses. perlu overload
        double* operator[] (int i)
        {
            return data[i];
        }
   
        double get(int i, int j)
        {
            return data[i][j];
        }
        int getBaris()
        {
            return baris;
        }
        int getKolom()
        {
            return kolom;
        }

        //awalnya semua isinya sama dengan nol
        void clear()
        {
            //kita belum overload, jadi manual ngerjainnya
            for (int i=0; i<baris; i++)
            {
                for(int j=0; j<kolom; j++)
                {
                    data[i][j] = 0;
                }
            }
        }
    
    private:
        int baris;
        int kolom;
        double **data;
};

class dataset
{
    public:
        dataset(int jumlah_sampel) : num_sampel{jumlah_sampel}, container(jumlah_sampel, 10), teracak(jumlah_sampel, 10) 
        {
            calcDelta();
            sampling();
            shuffling(); //langsung aja ya.
        } //nggak perlu parametric constructor lah ya.

        void calcDelta()
        {//parameter ditulis satu-satu biar nggak bikin bingung mana yang mana
            dy0 = (y0max-y0min)/(num_sampel+1);
            dxinter = (xintermax-xintermin)/(num_sampel+1);
            dy1 = (y1max - y1min)/(num_sampel+1);
            dx4 = (x4max - x4min)/(num_sampel+1);
            dy4 = (y4max - y4min)/(num_sampel+1);
            dy5 = (y5max - y5min)/(num_sampel+1);
            dw0 = (w0max - w0min)/(num_sampel+1);
            dwinter = (wintermax - wintermin)/(num_sampel+1);
            dw1 = (w1max - w1min)/(num_sampel+1);
            dw4 = (w4max - w4min)/(num_sampel+1);
        }
        //lanjut sampling di setiap interval
        void sampling()
        {
            double y0awal = y0min; 
            double xinterawal = xintermin;
            double y1awal = y1min;
            double x4awal = x4min;
            double y4awal = y4min;
            double y5awal = y5min;
            double w0awal = w0min;
            double winterawal = wintermin;
            double w1awal = w1min;
            double w4awal = w4min; 
            for(int i=0; i<num_sampel; i++)
            {//untuk kolom, mengikuti urutan yang sudah ditulis di bagian private
                double y0 = y0awal + dy0*(i+acak.munculkan()); container[i][0] = y0;
                double xinter = xinterawal + dxinter*(i+acak.munculkan()); container[i][1] = xinter;
                double y1 = y1awal + dy1*(i+acak.munculkan()); container[i][2] = y1;
                double x4 = x4awal + dx4*(i+acak.munculkan()); container[i][3] = x4;
                double y4 = y4awal + dy4*(i+acak.munculkan()); container[i][4] = y4;
                double y5 = y5awal + dy5*(i+acak.munculkan()); container[i][5] = y5;
                double w0 = w0awal + dw0*(i+acak.munculkan()); container[i][6] = w0;
                double winter = winterawal + dwinter*(i+acak.munculkan()); container[i][7] = winter;
                double w1 = w1awal + dw1*(i+acak.munculkan()); container[i][8] = w1;
                double w4 = w4awal + dw4*(i+acak.munculkan()); container[i][9] = w4;
            }
        }
        //terus ngambil matriksnya gimana ya? antara bikin matriks baru, atau Matriks container 
        Matriks container;
        Matriks teracak;
        void shuffling()
        {
            for (int i=0; i<10; i++) //10 itu jumlah barisnya
            {
                std::vector<int> indeks(num_sampel);
                for (int n=0; n<num_sampel; n++)
                {
                    indeks[n]=n;
                }
                acak.shuffle(indeks.begin(), indeks.end()); //kok kayaknya agak nggak efisien ya. lambat nggak ya.
                for (int n=0; n<num_sampel; n++)
                {
                    teracak[n][i] = container[indeks[n]][i];
                }
            }
        }

        std::vector<std::vector<double>> bacaData(std::string nama) //ini soalnya ukuran baris sama kolomnya nggak fix ya
        {
            //buka file csv pakai stringstream
            std::stringstream namafile;
            namafile << nama;
            std::ifstream baca(namafile.str());
            if (!baca.is_open())
            {
                std::cerr << "Error, tidak dapat membuka file" << std::endl;
            }
            std::vector<std::vector<double>> container;
            std::string line; //sekedar placeholder aja kali ya
            while (std::getline(baca, line)) //ini iterasi bari skan
            {
                std::istringstream sstream(line); //ini mestinya iterasi kolom
                std::string token;
                std::vector<double> row;
                //split baris menggunakan koma
                while (std::getline(sstream, token, ','))
                {
                    try //konversi token menjadi double precision floating point
                    {
                        double value = std::stod(token);
                        row.push_back(value);
                    }
                    catch (const std::exception& e)
                    {
                        std::cerr << "Error konversi: " << e.what() << " untuk token" << token << std::endl;
                    }
                }
                container.push_back(row);
            }
            baca.close();
            return container;
        }

    private: //penamaannya masih mengikuti yang versi lama ya
        double y0max = 150; double y0min = 110; double dy0;
        double xintermax = 50; double xintermin = 20; double dxinter; //ini xintermin nya sengaja dibikin lebih kecil, cavity sempit
        double y1max = 120; double y1min = 85; double dy1;
        double x4max = 15; double x4min = 5; double dx4;
        double y4max = 40; double y4min = 20; double dy4;
        double y5max = 10; double y5min = 5; double dy5;
        //bobot maksimal nya 5 kali ya. angka terkecilnya kayaknya jangan diset sama dengan nol. set 0.1 aja
        double w0min = 0.1; double w0max = 5; double dw0;
        double wintermin = 0.1; double wintermax = 2.5; double dwinter;
        double w1min = 0.1; double w1max = 5; double dw1;
        double w4min = 0.1; double w4max = 5; double dw4;

        int num_sampel;
        Rnd acak;

};

#endif