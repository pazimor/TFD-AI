import {
  Component,
  inject,
  OnInit, viewChild,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BuildComponent } from './build/build.component';
import { LanguageListComponent } from './langlist/language-list.component';
import { ModuleBankComponent } from './module-bank/module-bank.component';
import {sidebarComponent} from './sidebar/sidebar.component';


@Component({
  imports: [CommonModule, FormsModule, BuildComponent, LanguageListComponent, ModuleBankComponent, LanguageListComponent, sidebarComponent],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss', './module/modules-tiers.scss']
})
export class AppComponent {
  @ViewChild(BuildComponent) buildComponent!: BuildComponent;
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;
  @ViewChild(ModuleBankComponent) moduleBankComponent!: ModuleBankComponent;

  title = 'TFD-front';
}
