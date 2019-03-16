import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SigninComponent } from './signin/signin.component'; 
// import { LandingpageModule } from '../landingpage/landingpage.module';
import { FooterModule } from '../shared/modules/footer.module';


@NgModule({
  declarations: [SigninComponent ,],

  imports: [
    CommonModule
    ,FooterModule
      
  ]
})
export class SigninPageModule { }
