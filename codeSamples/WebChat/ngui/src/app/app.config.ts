import { ApplicationConfig, importProvidersFrom, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient, withFetch, withInterceptorsFromDi } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes), 
    provideClientHydration(withEventReplay()), 
    provideAnimationsAsync()
    // , importProvidersFrom(HomeComponent) // **MB: NO, instead:
    // , provideHttpClient(withInterceptorsFromDi()) // **MB copilot eventual suggestion, not too bad but went round a big loop
    , provideHttpClient(withFetch()) // **MB Copilot TRY n (!)
  ]
};
