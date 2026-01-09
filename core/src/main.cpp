#include "../include/ResourceEmitter.h"
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    ResourceEmitter emitter;

    std::thread commandThread(&ResourceEmitter::listenForCommands, &emitter);
    commandThread.detach();

    std::cout << "[ACTIVE] Broadcasting data to Aegis Mind..." << std::endl;

    while (true) {
        std::string payload = emitter.generatePayload();
        emitter.sendData(payload);
        
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    return 0;
}