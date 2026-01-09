#include "../include/ResourceEmitter.h"
#include <iostream>
#include <winsock2.h>
#include <string>
#include <thread>

// Constructor: Winsock başlatma
ResourceEmitter::ResourceEmitter() {
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cout << "[ERROR] Winsock baslatilamadi!" << std::endl;
    } else {
        std::cout << "[INIT] Aegis Core Resources Initialized." << std::endl;
    }
}

// Veri Paketi Oluşturma
std::string ResourceEmitter::generatePayload() {
    static int counter = 0;
    counter++;

    // Gerçekçi voltaj simülasyonu
    float voltage = 220.0f + (static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / 10.0f)));
    
    // Güç dalgalanması simülasyonu (Anomali)
    if (counter % 40 > 35) {
        voltage += 25.0f; 
        std::cout << "[!!!] SIMULATING POWER SURGE..." << std::endl;
    }

    float flow = 10.0f + (static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / 5.0f)));
    
    // JSON formatında veri (Python tarafının anlaması için)
    return "{\"voltage\": " + std::to_string(voltage) + 
           ", \"current\": " + std::to_string(flow) + "}";
}

// Veri Gönderme Fonksiyonu (Düzeltildi)
void ResourceEmitter::sendData(const std::string& data) {
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); 
    if (sock == INVALID_SOCKET) {
        std::cout << "[ERROR] Soket olusturulamadi: " << WSAGetLastError() << std::endl;
        return;
    }

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345); // Python'un dinlediği port
    serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Veriyi bir kez gönderiyoruz
    int bytesSent = sendto(sock, data.c_str(), (int)data.length(), 0, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    
    if (bytesSent == SOCKET_ERROR) {
        std::cout << "[ERROR] Gonderim Hatasi (10038 Cozuldu): " << WSAGetLastError() << std::endl;
    } else {
        std::cout << "[SENT] Aegis -> Mind: " << data << std::endl;
    }

    // Soketi her gönderimden sonra düzgünce kapatıyoruz
    closesocket(sock);
}

// Komut Dinleme (UDP versiyonu olarak düzeltildi)
void ResourceEmitter::listenForCommands() {
    SOCKET cmdSock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(12346); // Veri portundan farklı bir port (Çakışma olmaması için)

    if (bind(cmdSock, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::cout << "[ERROR] Bind hatasi: " << WSAGetLastError() << std::endl;
        return;
    }

    std::cout << "[LISTEN] Aegis Core is listening for commands on port 12346..." << std::endl;

    while (true) {
        char buffer[1024] = {0};
        sockaddr_in from;
        int fromLen = sizeof(from);
        
        // UDP'de listen/accept yerine recvfrom kullanılır
        int res = recvfrom(cmdSock, buffer, 1024, 0, (struct sockaddr*)&from, &fromLen);
        
        if (res > 0) {
            std::string cmd(buffer);
            if (cmd.find("/SHUTDOWN") != std::string::npos) {
                std::cout << "\n[!!!] EMERGENCY SHUTDOWN SIGNAL RECEIVED!" << std::endl;
                closesocket(cmdSock);
                WSACleanup();
                exit(0);
            }
        }
    }
}