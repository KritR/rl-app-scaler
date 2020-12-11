import http from 'k6/http';

export let options = {
  stages: [
    { duration: '5m', target: 10 }, // simulate ramp-up of traffic from 1 to 60 users over 5 minutes.
    { duration: '10m', target: 40 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 50 }, // ramp-up to 7 users
    { duration: '10m', target: 50 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 80 }, // ramp-up to 7 users
    { duration: '10m', target: 80 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 45 }, // ramp-up to 7 users
    { duration: '10m', target: 90 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 100 }, // continue at 60 for additional 10 minutes
    { duration: '2m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 7 }, // ramp-up to 7 users
    { duration: '10m', target: 70 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 40 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 80 }, // simulate ramp-up of traffic from 1 to 60 users over 5 minutes.
    { duration: '10m', target: 12 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 18 }, // ramp-up to 7 users
    { duration: '10m', target: 90 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 52 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 47 }, // ramp-up to 7 users
    { duration: '10m', target: 66 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 48 }, // ramp-up to 7 users
    { duration: '10m', target: 10 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
    { duration: '5m', target: 3 }, // stay-at to 3 users
    { duration: '5m', target: 7 }, // ramp-up to 7 users
    { duration: '10m', target: 10 }, // stay at 60 users for 10 minutes
    { duration: '3m', target: 5 }, // ramp-up to 100 users over 3 minutes (peak hour starts)
    { duration: '10m', target: 2 }, // stay at 100 users for short amount of time (peak hour)
    { duration: '1m', target: 1 }, // ramp-down to 60 users over 3 minutes (peak hour ends)
    { duration: '10m', target: 1 }, // continue at 60 for additional 10 minutes
    { duration: '5m', target: 3 }, // ramp-down to 0 users
  ],
};

export default function () {
  http.get('http://localhost:5000/');
}
