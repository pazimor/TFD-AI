import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BuildCardComponent } from './build-card.component';
import { buildListStore } from '../../store/build-list.store';
import { loginStore } from '../../store/login.store';

@Component({
  standalone: true,
  selector: 'saved-builds',
  imports: [CommonModule, BuildCardComponent],
  templateUrl: './saved-builds.component.html',
  styleUrls: ['./saved-builds.component.scss']
})
export class SavedBuildsComponent implements OnInit {
  readonly list_store = inject(buildListStore);
  readonly login = inject(loginStore);

  ngOnInit(): void {
    const uid = this.login.user()?.id;
    if (uid) {
      this.list_store.load(uid);
    }
  }

  builds = this.list_store.builds;
}
