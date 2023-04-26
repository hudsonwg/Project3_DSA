#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;

struct Media
{
public:

    string tconst;
    string titletype;
    string primarytitle;
    string originaltitle;
    bool isadult;
    int startyear;
    int endyear;
    int runtimeminutes;
    string genres;

    Media(string TCONST, string TITLETYPE, string PRIMARYTITLE, string ORIGINALTITLE, bool ISADULT, int STARTYEAR, int ENDYEAR, int RUNTIMEMINUTES, string GENRES)
    {
        tconst = TCONST;
        titletype = TITLETYPE;
        primarytitle = PRIMARYTITLE;
        originaltitle = ORIGINALTITLE;
        isadult = ISADULT;
        startyear = STARTYEAR;
        endyear = ENDYEAR;
        runtimeminutes = RUNTIMEMINUTES;
        genres = GENRES;
    }
    void display()
    {
        cout << tconst << " " << titletype << " " << primarytitle << " " << originaltitle << " " << isadult << " " << startyear << " " << endyear << " " << runtimeminutes << " " << genres;
        cout << endl;
    }
};

int main()
{
    ifstream inputFile;
    inputFile.open("data.csv");

    if (inputFile.is_open())
    {
        cout << "file is open" << endl;
    }
    else
    {
        cout << "file didnt open" << endl;
    }

    string line = "";

    vector<Media> medialist;
    getline(inputFile, line); //remove header
    line = "";

    cout << "starting" << endl;

    while (getline(inputFile, line))
    {

        string tconst;
        string titletype;
        string primarytitle;
        string originaltitle;
        bool isadult;
        int startyear;
        int endyear;
        int runtimeminutes;
        string genres;
        string tempString;

        stringstream inputString(line);

        getline(inputString, tconst, ',');
        getline(inputString, titletype, ',');
        getline(inputString, primarytitle, ',');
        getline(inputString, originaltitle, ',');


        getline(inputString, tempString, ',');
        isadult = atoi(tempString.c_str());
        tempString = "";

        getline(inputString, tempString, ',');
        startyear = atoi(tempString.c_str());
        tempString = "";

        getline(inputString, tempString, ',');
        endyear = atoi(tempString.c_str());
        tempString = "";

        getline(inputString, tempString, ',');
        runtimeminutes = atoi(tempString.c_str());
        tempString = "";

        getline(inputString, genres, ',');
        getline(inputString, tempString, ',');


        Media mediadetail(tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres);

        medialist.push_back(mediadetail);

        line = "";
    }

    for (auto media : medialist)
    {
        media.display();
    }

    cout << "done" << endl;


    return 0;
}