#ifndef ACCELERATOR_H_
#define ACCELERATOR_H_


#include <Arduino.h>


//============
class Accelerator {
    private:
        // times in seconds, distances in cm
        float target_speed, alpha, beta, A, B, T, prev_t, current_t;
        unsigned long start_t;
        bool is_running;
        
        void constantAcceleration(float& progress_speed);
        void smoothAcceleration(float& progress_speed);
        float uniformProfile();
        float trapezoidProfile(float t);
        float integralTrapezoidProfile(float t);

    public: 
        Accelerator(float alpha=0);
        void start(float progress_speed, float target_speed, float T);
        void stop();
        void accelerate(float& progress_speed);  
        bool saturation(const float& progress_speed);  
        void Accelerator::yo(float& T,float& beta,float& alpha,float& B, float& t, float& a)  {
            T=this->T;beta=this->beta;alpha=this->alpha;B=A / (1-this->alpha);
            t = this->prev_t;
            a = this->integralTrapezoidProfile(this->prev_t);
        }   
};


#endif  // ACCELERATOR_H_