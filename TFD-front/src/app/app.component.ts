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
import { appStore } from './store/data.store';
import { ModuleBankComponent } from './module-bank/module-bank.component';
import { CharacterComponent } from './character/character.component';
import {sidebarComponent} from './sidebar/sidebar.component';


@Component({
  imports: [CommonModule, FormsModule, BuildComponent, LanguageListComponent, ModuleBankComponent, LanguageListComponent, CharacterComponent, sidebarComponent],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss', './module/modules-tiers.scss']
})
export class AppComponent {
  @ViewChild(BuildComponent) buildComponent!: BuildComponent;
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;
  @ViewChild(ModuleBankComponent) moduleBankComponent!: ModuleBankComponent;
  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;

  title = 'TFD-front';
}
