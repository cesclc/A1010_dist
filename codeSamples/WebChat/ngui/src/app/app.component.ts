import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SettingsComponent } from './settings/settings.component';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [SettingsComponent, HomeComponent,  CommonModule]
})
export class AppComponent { 
  showSettings: boolean = false;

  toggleSettings() { 
    this.showSettings = !this.showSettings;
  }
}  
