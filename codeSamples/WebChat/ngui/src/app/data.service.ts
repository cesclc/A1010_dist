// import { Injectable } from '@angular/core';

// @Injectable({
//   providedIn: 'root'
// })
// export class DataService {

//   constructor() { }
// }


import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpHeaders, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { console } from 'inspector';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  sendData(data: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/send`, { data });
  }

  getSettings(): Observable<any> {
    return this.http.get(`${this.apiUrl}/settings`);
  }

  selectItem(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/select`, { id });
  }

  streamData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/stream`, { responseType: 'text', observe: 'response' });
  }

  getStatus(): Observable<any> {
    return this.http.get(`${this.apiUrl}/status`, { responseType: 'text', observe: 'response' });
  }
}
