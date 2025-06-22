import { Component, Inject, inject, effect, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { dataStore, defaultTranslate, TranslationString, BoardNode, Boards, NodeEffect } from '../../../store/data.store';
import { visualStore } from '../../../store/display.store';
import { getTranslationField } from '../../../lang.utils';
import { DescendantsResponse } from '../../../types/descendant.types';

@Component({
  standalone: true,
  selector: 'archeron-tree',
  imports: [CommonModule, MatDialogModule, MatButtonModule],
  templateUrl: './archeron-tree.component.html',
  styleUrls: ['./archeron-tree.component.scss']
})
export class ArcheronTreeComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  board?: Boards;
  hoverName = signal('');
  hoverEffects = signal<NodeEffect[]>([]);
  active = signal(new Set<string>());
  readonly MAX_ACTIVE = 40;   // Limite maximale de cases actives en même temps

  key(node: BoardNode): string {
    return `${node.position_row}-${node.position_column}`;
  }

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { descendant: DescendantsResponse; nodes: number[] },
    private dialogRef: MatDialogRef<ArcheronTreeComponent>
  ) {
    this.data_store.load_boards();
    effect(() => {
      this.board = computed(() => this.data_store.BoardResource.value() ?? [])()[1];
      this.board = this.shiftBoard(this.board);
      if (this.board && this.data.nodes?.length) {
        const set = new Set<string>();
        this.data.nodes.forEach(id => {
          const n = this.board!.nodes.find(node => node.node_id === id);
          if (n) set.add(this.key(n));
        });
        this.active.set(set);
      }
    });
  };

  shiftBoard = (board: Boards): Boards => ({
    ...board,
    nodes: board.nodes.map(node => ({
      ...node,
      position_row: node.position_row + 1,
      position_column: node.position_column + 1,
    }))
  });

  toggle(node: BoardNode): void {
    if (!this.board) return;

    const set = new Set(this.active());
    const key = this.key(node);
    const isActive = set.has(key);

    if (isActive) {
      set.delete(key);

      for (const n of this.board.nodes) {
        const k = this.key(n);
        if (
          set.has(k) &&
          n.node_type?.toLowerCase() !== 'start' &&
          !this.pathExistsWithSet(n, set)
        ) {
          return;
        }
      }

      this.active.set(set);
    } else {
      if (!this.canActivate(node)) return;
      set.add(key);
      this.active.set(set);
    }
  }

  private neighbors(node: BoardNode): BoardNode[] {
    if (!this.board) return [];
    return this.board.nodes.filter(n =>
      Math.abs(n.position_row - node.position_row) + Math.abs(n.position_column - node.position_column) === 1
    );
  }

  canActivate(node: BoardNode): boolean {
    if (!this.board) return false;
    if (node.node_type?.toLowerCase() === 'start') return true;

    if (this.active().size >= this.MAX_ACTIVE) return false;

    return this.neighbors(node).some(
      n =>
        n.node_type?.toLowerCase() === 'start' ||
        this.active().has(this.key(n))
    );
  }

  private pathExistsWithSet(target: BoardNode, active: Set<string>): boolean {
    if (!this.board) return false;

    const start = this.board.nodes.find(
      n => n.node_type?.toLowerCase() === 'start'
    );
    if (!start) return false;

    const visited = new Set<string>();
    const stack: BoardNode[] = [start];

    while (stack.length) {
      const current = stack.pop()!;
      const currentKey = this.key(current);
      if (currentKey === this.key(target)) return true;
      visited.add(currentKey);

      for (const neigh of this.neighbors(current)) {
        const k = this.key(neigh);
        if (!visited.has(k) && (k === this.key(target) || active.has(k))) {
          stack.push(neigh);
        }
      }
    }

    return false;
  }

  updateInfo(node: BoardNode): void {
    const langKey = getTranslationField(this.visual_store.get_lang());
    const translations = this.data_store.translationResource.value();
    const tr: TranslationString = translations ? translations[node.name_id - 1] : defaultTranslate;
    this.hoverName.set((tr as any)[langKey] ?? '');
    this.hoverEffects.set(node.effects);
  }

  confirmSelection(): void {
    if (!this.board) {
      this.dialogRef.close([]);
      return;
    }
    const ids = Array.from(this.active()).map(key => {
      const [r, c] = key.split('-').map(Number);
      const n = this.board!.nodes.find(node => node.position_row === r && node.position_column === c);
      return n?.node_id ?? 0;
    }).filter(id => id !== 0);
    this.dialogRef.close(ids);
  }
}
