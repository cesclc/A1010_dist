// import { Component } from '@angular/core';

// @Component({
//   selector: 'app-settings',
//   imports: [],
//   templateUrl: './settings.component.html',
//   styleUrl: './settings.component.css'
// })
// export class SettingsComponent {

// }


import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css'],
  imports: [CommonModule]
})
export class SettingsComponent implements OnInit {
  settingsData: any[] = [];
  selectedId: number | null = null;
  credit: number = 100;
  creditColor = "blue";

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.dataService.getSettings().subscribe(data => {
      this.settingsData = data;
    });

    this.dataService.getStatus().subscribe(event => {
      if (event.type === 3) { // HttpEventType.Response
        this.credit = parseInt(event.body, 10);
      }
    });
  }

  selectItem(id: number) {
    this.selectedId = id;
    this.dataService.selectItem(id).subscribe(response => {
      console.log(response.message);
    });
  }

  sortData(field: string) {
    this.settingsData.sort((a, b) => {
      if (a[field] < b[field]) return -1;
      if (a[field] > b[field]) return 1;
      return 0;
    });
  }

  reverseSortData(field: string) {
    this.settingsData.sort((a, b) => {
      if (a[field] > b[field]) return -1;
      if (a[field] < b[field]) return 1;
      return 0;
    });
  }
} 
