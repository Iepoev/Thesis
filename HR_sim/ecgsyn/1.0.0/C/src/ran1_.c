/* File:      ran1.C
   Date:      01/04/02  (written fall 2001)
   Author:    C. Paciorek - taken from Numerical Recipes in C
   Purpose:   random uniform generator
   Compile:   g++ -c
   Usage:     
   Arguments: 
   Requires:  
   Reference: Numerical Recipes in C 
*/
#include "base.h" 



#define IA 16807 
#define IM 2147483647 
#define AM (1.0/IM) 
#define IQ 127773 
#define IR 2836 
#define NTAB 32 
#define NDIV (1+(IM-1)/NTAB) 
#define EPS 1.2e-7 
#define RNMX (1.0-EPS) 

float ran1(int *idum,int mode,char* line){ /*\Minimal" random number generator of Park and Miller with Bays-Durham shu e and added safeguards. Returns a uniform random deviate between 0.0 and 1.0 (exclusive of the endpoint values). Call with idum a negative integer to initialize; thereafter, do not alter idum between successive deviates in a sequence. RNMX should approximate the largest oating value that is less than 1. */
  int j; int k; 
  static int iy=0; 
  static int iv[NTAB]; 
 float temp; 

 if(mode==GENERATE){
   if (*idum <= 0 || !iy) { //Initialize. 
     if (-(*idum) < 1) *idum=1; //Be sure to prevent idum = 0. 
     else *idum = -(*idum); 
     for (j=NTAB+7;j>=0;j--) { // Load the shu e table (after 8 warm-ups). 
       k=(*idum)/IQ; 
       *idum=IA*(*idum-k*IQ)-IR*k; 
       if (*idum < 0) *idum += IM; 
       if (j < NTAB) iv[j] = *idum; } 
     iy=iv[0]; } 
   k=(*idum)/IQ; //Start here when not initializing. 
   *idum=IA*(*idum-k*IQ)-IR*k; //Compute idum=(IA*idum) % IM without over- ows by Schrage's method. 
   if (*idum < 0) *idum += IM; 
   j=iy/NDIV; //Will be in the range 0..NTAB-1. 
   iy=iv[j]; //Output previously stored value and re ll the shu e table. 
   iv[j] = *idum; 
   if ((temp=AM*iy) > RNMX) return RNMX; //Because users don't expect endpoint values. 
   else return temp; 
 } 
 if(mode==WRITE){
   ostrstream buffer(line,1024);
   buffer << *idum << " " << iy;
   for(j=0;j<NTAB;j++){
     buffer << " " << iv[j];
   }
   buffer << endl;
 }
 if(mode==READ){
   istrstream buffer(line,1024);
   buffer  >> iy;
   for(j=0;j<NTAB;j++){
     buffer >> iv[j];
   }
 }
 return(0);
}

