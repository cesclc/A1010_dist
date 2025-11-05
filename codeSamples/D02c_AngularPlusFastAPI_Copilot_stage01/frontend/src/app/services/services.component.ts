import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-services',
  templateUrl: './services.component.html',
  styleUrls: ['./services.component.css']
})
export class ServicesComponent {
  services = ['Training','Consultancy','Authoring','Mentoring','Coaching'];
  constructor(private router: Router) {}
  select(s: string){
    // for now just alert and navigate home
    alert('You selected: ' + s);
    this.router.navigate(['/']);
  }
}
