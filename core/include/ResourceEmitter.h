#ifndef RESOURCE_EMITTER_H
#define RESOURCE_EMITTER_H

#include <string>
#include <atomic> 

class ResourceEmitter {
public:
    ResourceEmitter();
    std::string generatePayload();
    void sendData(const std::string& data);
    void listenForCommands(); 
    
    std::atomic<bool> isRunning; 

private:
    float currentVoltage;
    float waterFlow;
};

#endif