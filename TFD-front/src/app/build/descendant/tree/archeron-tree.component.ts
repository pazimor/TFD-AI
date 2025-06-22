import { Component, Inject, inject, effect, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { dataStore, defaultTranslate, TranslationString, BoardNode, Boards, NodeEffect } from '../../../store/data.store';
import { visualStore } from '../../../store/display.store';
import { getTranslationField } from '../../../lang.utils';
import { DescendantsResponse } from '../../../types/descendant.types';

@Component({
  standalone: true,
  selector: 'archeron-tree',
  imports: [CommonModule, MatDialogModule],
  templateUrl: './archeron-tree.component.html',
  styleUrls: ['./archeron-tree.component.scss']
})
export class ArcheronTreeComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  board?: Boards;
  active = signal(new Set<number>());
  hoverName = signal('');
  hoverEffects = signal<NodeEffect[]>([]);

  constructor(@Inject(MAT_DIALOG_DATA) public descendant: DescendantsResponse) {
    this.data_store.load_boards();
    effect(() => {
      const boards = this.data_store.BoardResource.value() ?? [];
      this.board = boards.find((b: Boards) => b.board_group_id === descendant.descendant_group_id);
    });
  }

  toggle(node: BoardNode): void {
    if (!this.canActivate(node)) {
      return;
    }
    const set = new Set(this.active());
    if (set.has(node.node_id)) {
      set.delete(node.node_id);
    } else {
      set.add(node.node_id);
    }
    this.active.set(set);
  }

  private neighbors(node: BoardNode): BoardNode[] {
    if (!this.board) return [];
    return this.board.nodes.filter(n =>
      Math.abs(n.position_row - node.position_row) + Math.abs(n.position_column - node.position_column) === 1
    );
  }

  private pathExists(target: BoardNode): boolean {
    if (!this.board) return false;
    const starts = this.board.nodes.filter(n => n.node_type?.toLowerCase() === 'start');
    const visited = new Set<number>();
    const stack = [...starts];
    const active = this.active();
    while (stack.length) {
      const current = stack.pop()!;
      if (current.node_id === target.node_id) return true;
      visited.add(current.node_id);
      for (const n of this.neighbors(current)) {
        if ((active.has(n.node_id) || n.node_id === target.node_id) && !visited.has(n.node_id)) {
          stack.push(n);
        }
      }
    }
    return false;
  }

  canActivate(node: BoardNode): boolean {
    if (!this.board) return false;
    if (node.node_type?.toLowerCase() === 'start') return true;
    return this.pathExists(node);
  }

  updateInfo(node: BoardNode): void {
    const langKey = getTranslationField(this.visual_store.get_lang());
    const translations = this.data_store.translationResource.value();
    const tr: TranslationString = translations ? translations[node.name_id - 1] : defaultTranslate;
    this.hoverName.set((tr as any)[langKey] ?? '');
    this.hoverEffects.set(node.effects);
  }
}
