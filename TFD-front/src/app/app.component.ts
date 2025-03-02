import {
  Component,
  inject,
  Signal,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BuildComponent } from './build/build.component';
import { LanguageListComponent } from './langlist/language-list.component';
import { ModuleBankComponent } from './module-bank/module-bank.component';
import {sidebarComponent} from './sidebar/sidebar.component';
import {appStore} from './store/data.store';


@Component({
  imports: [CommonModule, FormsModule, BuildComponent, LanguageListComponent, ModuleBankComponent, LanguageListComponent, sidebarComponent],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  @ViewChild(BuildComponent) buildComponent!: BuildComponent;
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;
  @ViewChild(ModuleBankComponent) moduleBankComponent!: ModuleBankComponent;

  readonly store = inject(appStore);
  title = 'TFD-front';

  isSidebarOpen$$: Signal<boolean> = this.store.isSidebarOpen
}
