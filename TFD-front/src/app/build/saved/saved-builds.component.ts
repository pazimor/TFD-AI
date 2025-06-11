import { Component, inject, signal, WritableSignal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { loginStore } from '../../store/login.store';
import { buildStore } from '../../store/build.store';
import { BuildCardComponent, BuildSummary } from './build-card/build-card.component';
import { environment } from '../../../env/environment';
import { Router } from '@angular/router';
import { buildListStore } from '../../store/build-list.store';
import { dataStore } from '../../store/data.store';
import { defaultDescendants } from '../../types/descendant.types';
import { defaultModule } from '../../types/module.types';
import { defaultWeapon } from '../../types/weapon.types';
import { defaultReactor } from '../../types/reactor.types';
import { defaultExternalComponent } from '../../types/external.types';

@Component({
  selector: 'saved-builds-list',
  imports: [CommonModule, BuildCardComponent], // BuildCardComponent added
  templateUrl: './saved-builds.component.html',
  styleUrls: ['./saved-builds.component.scss']
})
export class SavedBuildsListComponent {
  private buildListStore = inject(buildListStore)
  private loginStore = inject(loginStore);
  private buildStore = inject(buildStore);
  private dataStore = inject(dataStore)
  //private router = inject(Router); // TODO: not use full now

  builds: WritableSignal<BuildSummary[]> = signal([]);
  isLoading = signal(false);
  errorLoading = signal<string | null>(null);

  constructor() {
    effect(() => {
      if (this.loginStore.loggedIn()) {
        const userId = this.loginStore.user()?.id;
        if (userId!) {
          this.buildListStore.load(userId)
        }
      }
    });

    effect(() => {
      if (this.buildStore.getBuildRessource.hasValue()) {
        const build = this.buildStore.getBuildRessource.value()!.build_data;
        const data = {
          descendant: this.dataStore.descendantResource.value()?.find(item => item.descendant_id === build.descendant) ?? defaultDescendants,
          descendantModules: build.descendantModules.map(id => this.dataStore.modulesResource.value()?.find(item => item.module_id === id) ?? defaultModule),
          weapons: build.weapons.map(id => this.dataStore.weaponResource.value()?.find(w => w.weapon_id === id) ?? defaultWeapon),
          weaponsModules: build.weaponsModules.map(slot => slot.map(id => this.dataStore.modulesResource.value()?.find(m => m.module_id === id) ?? defaultModule)),
          reactor: this.dataStore.reactorResource.value()?.find(item => item.reactor_id === build.reactor) ?? defaultReactor,
          externals: build.externals.map(id => this.dataStore.externalResource.value()?.find(e => e.external_component_id === id) ?? defaultExternalComponent),
        };
        console.log(data, build, this.dataStore.descendantResource.value())
        this.buildStore.hydrate(data);

        //TODO: update (this.module_data.descendant = res.descendant_id)
        //TODO: update (weapon number to display + descendant to display)
        //TODO: navigate to the build Maker Tab
      }
    });

    effect(() => {
      if (this.buildListStore.resource.hasValue()) {
        this.builds.set(this.buildListStore.resource.value());
      }
    });
  }

  LoadBuild(buildId: number): void {
    this.buildStore.loadFromApi(buildId);
  }

  refresh(): void {
    this.buildListStore.resource.reload()
  }
}
