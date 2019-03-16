import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SignupPageComponent } from './signup-page/signup-page.component';
// import { FooterModule } from '../shared/modules/footer.module';
import { FooterModule } from "@app/shared/modules/footer.module"

@NgModule({
  declarations: [SignupPageComponent],
  imports: [
    CommonModule,FooterModule
  ]
})
export class SignupModule { }
