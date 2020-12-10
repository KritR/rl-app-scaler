import http from 'k6/http';

export let options = {
//  vus: 10,
  iterations: 100,
};

export default function () {
  http.get('http://localhost:5000/');
}
