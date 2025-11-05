// import { Component } from '@angular/core';

// @Component({
//   selector: 'app-home',
//   imports: [],
//   templateUrl: './home.component.html',
//   styleUrl: './home.component.css'
// })
// export class HomeComponent {

// }


import { Component, NgZone, OnDestroy, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpEventType } from '@angular/common/http';
import { Subscription } from 'rxjs';
import {EventSource} from 'eventsource'; // **MB for streaming.TRY2


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  imports: [CommonModule, FormsModule
    // , HttpClientModule // NO, provideHttpClient... in (create!) home.module.ts instead
  ]
})
export class HomeComponent implements OnDestroy, OnInit {
  inputText: string = '';
  outputText: string = '';
  streamedData: string = '';
  private sseSub$?: Subscription;
  private evSource?: EventSource; 

  constructor(private dataService: DataService, private ngZone: NgZone) {}

  sendData() {
    this.dataService.sendData(this.inputText).subscribe(response => {
      this.outputText = response.reply;
    });
  }

  // streamData() {  // **MB streaming.TRY1
  //   this.sseSub$ = this.dataService.streamData().subscribe(event => {
  //     // Maybe look at event.status, event.body?
  //     var s = `Rx ev .type=${event.type} .status=${event.status} .body=${event.body}`;
  //     this.streamedData += s + '\n';
  //     var n = HttpEventType.Sent
  //     console.log(s);
  //     // event.type: Sent=0 UploadProgress=1 ResponseHeader=2 DownloadProgress=3
  //     //  Response=4 User=5
  //   }); 
  // }

  ngOnInit(): void {
    // this.streamData();  // **MB streaming.TRY
    // **MB try the below instead
    // **MB streaming.TRY2
    if (this.evSource) {
      this.evSource.close();
    }
    this.evSource = new EventSource('http://localhost:8000/stream');
    this.evSource.onmessage = (event) => {
      // var s = `Rx ev .type=${event.type} .status=${event.status} .body=${event.body}`;
      var s = `Rx ev .type=${event.type}`;
      var n = HttpEventType.Sent
      console.log(s);
      this.ngZone.run(() => {
        const data = JSON.parse(event.data);
        const s = JSON.stringify(data);
        console.log(s);
        this.streamedData += s + '\n';
      });
    };
  }

  ngOnDestroy(): void { 
    if (this.sseSub$) {
      this.sseSub$.unsubscribe();
    }
    if (this.evSource) {
      this.evSource.close();
    }
  }

} 
