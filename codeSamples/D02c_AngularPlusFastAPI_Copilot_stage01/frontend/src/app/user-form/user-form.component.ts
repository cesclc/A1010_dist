import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user-form',
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.css']
})
export class UserFormComponent {
  model = {
    name: '',
    address1: '',
    address2: '',
    postcode: '',
    email: '',
    phone: ''
  };
  message = '';

  constructor(private http: HttpClient) {}

  submit() {
    this.message = 'Sending...';
    this.http.post('http://localhost:8080/users', this.model)
      .subscribe({
        next: () => this.message = 'Submitted successfully',
        error: (err) => this.message = 'Error: ' + (err?.message || err)
      });
  }
}
