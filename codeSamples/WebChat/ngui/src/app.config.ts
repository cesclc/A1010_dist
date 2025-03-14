import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { DataService } from './app/data.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    DataService,
    // ... and any other providers 
  ]
};
