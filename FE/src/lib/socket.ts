import { io, Socket } from 'socket.io-client';

let socket: Socket | null = null;

export const initializeSocket = (householdId: number) => {
    if (socket) {
        socket.disconnect();
    }

    // Connect to backend WebSocket
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:6868';
    socket = io(baseUrl, {
        autoConnect: true
    });

    socket.on('connect', () => {
        console.log('Socket connected');
        // Join household room to receive notifications
        socket?.emit('join_household', { household_id: householdId });
    });

    socket.on('disconnect', () => {
        console.log('Socket disconnected');
    });

    return socket;
};

export const getSocket = () => socket;

export const disconnectSocket = () => {
    if (socket) {
        socket.disconnect();
        socket = null;
    }
};
