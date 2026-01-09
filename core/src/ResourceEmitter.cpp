#include "../include/ResourceEmitter.h"
#include <iostream>
#include <winsock2.h>
#include <string>
#include <thread>

// 1. CONSTRUCTOR (Hata veren ilk kısım buydu)
ResourceEmitter::ResourceEmitter() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
    std::cout << "[INIT] Aegis Core Resources Initialized." << std::endl;
}

std::string ResourceEmitter::generatePayload() {
    static int counter = 0;
    counter++;

    float voltage = 220.0f + (static_cast<float>(rand()) / (static_cast<float>(RAND_MAX/10.0f)));
    
    if (counter % 40 > 35) {
        voltage += 25.0f; 
        std::cout << "[!!!] SIMULATING POWER SURGE..." << std::endl;
    }

    float flow = 10.0f + (static_cast<float>(rand()) / (static_cast<float>(RAND_MAX/5.0f)));
    
    return "{\"voltage\": " + std::to_string(voltage) + 
           ", \"water_flow\": " + std::to_string(flow) + "}";
}
void ResourceEmitter::sendData(const std::string& data) {
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); 
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(6666);
    serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    sendto(sock, data.c_str(), data.length(), 0, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    
    closesocket(sock);
}

void ResourceEmitter::listenForCommands() {
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, 0);
    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(7777);

    bind(sock, (struct sockaddr*)&addr, sizeof(addr));
    listen(sock, 3);

    while (true) {
        SOCKET client = accept(sock, NULL, NULL);
        char buffer[1024] = {0};
        recv(client, buffer, 1024, 0);
        
        std::string cmd(buffer);
        if (cmd == "/SHUTDOWN") {
            std::cout << "\n[!!!] EMERGENCY SHUTDOWN SIGNAL RECEIVED FROM MIND!" << std::endl;
            exit(0);
        }
        closesocket(client);
    }
}