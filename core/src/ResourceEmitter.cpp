#include "../include/ResourceEmitter.h"
#include <iostream>
#include <winsock2.h>
#include <string>

ResourceEmitter::ResourceEmitter() {
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cout << "[ERROR] Winsock baslatilamadi!" << std::endl;
    } else {
        std::cout << "[INIT] Aegis Core Resources Initialized." << std::endl;
    }
}

std::string ResourceEmitter::generatePayload() {
    static int counter = 0;
    counter++;

    float voltage = 220.0f + (static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / 10.0f)));
    
    if (counter % 40 > 35) {
        voltage += 40.0f; 
        std::cout << "[!!!] SIMULATING POWER SURGE..." << std::endl;
    }

    float flow = 10.0f + (static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / 5.0f)));
    
    return "{\"voltage\": " + std::to_string(voltage) + 
            ", \"current\": " + std::to_string(flow) + "}";
}

void ResourceEmitter::sendData(const std::string& data) {
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); 
    if (sock == INVALID_SOCKET) return;

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345);
    serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    sendto(sock, data.c_str(), (int)data.length(), 0, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    
    closesocket(sock);
}

void ResourceEmitter::listenForCommands() {
    SOCKET cmdSock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    
    u_long mode = 1; 
    ioctlsocket(cmdSock, FIONBIO, &mode); 

    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(12346);

    bind(cmdSock, (struct sockaddr*)&addr, sizeof(addr));


    char buffer[1024] = {0};
    sockaddr_in from;
    int fromLen = sizeof(from);
    
    int res = recvfrom(cmdSock, buffer, 1024, 0, (struct sockaddr*)&from, &fromLen);
    
    if (res > 0) {
        std::string cmd(buffer);
        if (cmd.find("/SHUTDOWN") != std::string::npos) {
            std::cout << "\n[!!!] EMERGENCY SHUTDOWN SIGNAL RECEIVED FROM AI!" << std::endl;
            closesocket(cmdSock);
            WSACleanup();
            exit(0);
        }
    }
    closesocket(cmdSock); 
}